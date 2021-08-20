import torch
import torch.nn as nn
from torch.nn.modules.utils import _pair
import math

class DeformConv(nn.Module):

  def __init__(self,
             in_channels,
             out_channels,
             kernel_size,
             stride=1,
             padding=1,
             dilation=1,
             groups=1,
             deformable_groups=1,
             bias=False):
                 
    super(DeformConv, self).__init__()

    assert not bias
    assert groups == 1, 'Not support group larger than 1'
    assert dilation == 1
            

    self.in_channels = in_channels
    self.out_channels = out_channels
    self.kernel_size = _pair(kernel_size)
    self.stride = _pair(stride)
    self.padding = _pair(padding)
    self.dilation = _pair(dilation)
    self.groups = groups
    self.deformable_groups = deformable_groups

    self.weight = nn.Parameter(
        torch.Tensor(out_channels, in_channels,
                     *self.kernel_size))

    self.reset_parameters()
    
    # manually set device if necessary
    self.device = 'cuda' if torch.cuda.is_available() else 'cpu' 
       
    self.coord = None
        
  def reset_parameters(self):
    n = self.in_channels
    for k in self.kernel_size:
      n *= k
    stdv = 1. / math.sqrt(n)
    self.weight.data.uniform_(-stdv, stdv)
    
  def _cache_at_first_time_run(self, h, w):
    low = - (self.kernel_size[0]//2)
    hi  = self.kernel_size[0]//2
    grid_i, grid_j = torch.meshgrid(torch.arange(low, h+hi, device=self.device),
                                        torch.arange(low, w+hi, device=self.device))
    self.coord = torch.cat((grid_i.unsqueeze(2), grid_j.unsqueeze(2)), 2) # h+2 x w+2 x 2
    
    # check out im2col procedure for more information
    self.coord = torch.as_strided(self.coord, size = (h, w, *self.kernel_size, 2),
                                  stride=(*((self.coord.stride(0), self.coord.stride(1))*2),
                                          self.coord.stride(2)) )
    self.coord = self.coord.contiguous().view(1, h, w, -1, 2).float()
    self.coord.requires_grad = False
      
  def forward(self, x, offset):
    '''
    x: input Tensor of shape [N x C x H x W]
    offset: Tensor of shape [N x 18 x H x W] for 3x3 cnn kernel
    the "18" dimension are offset coordinates, arranged in order:
    
     ((tlh, tlw), (tmh, tmw), (trh, trw),
      (mlh, mlw), (mmh, mmw), (mrh, mrw),
      (blh, blw), (bmh, bmw), (brh, brw))
      
      t: top, m: middle, b: bottom
      l: left, r: right
      h: hight or i, w: width or j
      
      note:
        bilinear interpolation with proximity outside of image are set to 0 (not the interpolated point)
    '''
    b, c, h, w = x.shape
    if self.coord is None:
      self._cache_at_first_time_run(h,w)
      
    
    offset = offset.view(b, self.kernel_size[0]**2, 2, h, w).permute([0,3,4,1,2]) # b, h, w, 9, 2
    print(offset.shape, self.coord.shape)
    coord = offset + self.coord
    
    coord_lt = coord.floor().long() # b, h, w, 9, 2
    coord_rb = coord.ceil().long()
    coord_rt = torch.stack([coord_lt[..., 0], coord_rb[..., 1]], -1)
    coord_lb = torch.stack([coord_rb[..., 0], coord_lt[..., 1]], -1)
    
    vals_lt = self._sampling(x, coord_lt.detach())
    vals_rb = self._sampling(x, coord_rb.detach())
    vals_lb = self._sampling(x, coord_lb.detach())
    vals_rt = self._sampling(x, coord_rt.detach())
    
    fract = coord - coord_lt.float()
    fract = fract.unsqueeze(1)
    vals_t = self._interpolate(vals_lt, vals_rt, fract[..., 1])
    vals_b = self._interpolate(vals_lb, vals_rb, fract[..., 1])
    
    mapped_vals = self._interpolate(vals_t, vals_b, fract[..., 0])
    mapped_vals = mapped_vals.permute([1, 4, 0, 2, 3]).reshape(-1, b*h*w)
    output = torch.matmul(self.weight.view(self.out_channels, -1), mapped_vals) # C' x (B x H x W)
    
    return output.view(self.out_channels, b, h, w).permute([1,0,2,3])
      
  def _sampling(self, x: torch.Tensor, coord: torch.Tensor):
    b, c, h, w = x.shape
    # coord : b, h, w, 9, 2
    k = self.kernel_size[0]**2
    coord = coord.reshape(b, 1, -1, 2).repeat(1,c,1,1).view(b*c, -1, 2)
    outside = (coord[..., 0] >= h) + (coord[..., 0] < 0) + \
              (coord[..., 1] >= w) + (coord[..., 1] < 0)
    
    indx = coord[..., 0]*w + coord[..., 1] + \
            (h*w*torch.arange(c*b, device=self.device)).view(-1, 1)
    x = x.view(-1).index_select(0, indx.view(-1).clamp(0, b*c*h*w-1))
    x[outside.view(-1)] = 0
    return x.reshape(b, c, h, w, k)  
    
  @staticmethod    
  def _interpolate(x: torch.Tensor, y: torch.Tensor, frac: torch.Tensor):
    '''
    Linear interpolation between x and y
    Sub-routine for bi-linear interpolation
    '''
    return x + frac*(y-x)
    
class ModulatedDeformConv(nn.Module):

  def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 stride=1,
                 padding=1,
                 dilation=1,
                 groups=1,
                 deformable_groups=1,
                 bias=True):
    
    assert deformable_groups == 1
    assert groups == 1
    
    super(ModulatedDeformConv, self).__init__()
    self.in_channels = in_channels
    self.out_channels = out_channels
    self.kernel_size = _pair(kernel_size)
    self.stride = stride
    self.padding = padding
    self.dilation = dilation
    self.groups = groups
    self.deformable_groups = deformable_groups
    self.with_bias = bias

    self.weight = nn.Parameter(
      torch.Tensor(out_channels, in_channels // groups,
                   *self.kernel_size))
    if bias:
      self.bias = nn.Parameter(torch.Tensor(out_channels))
    else:
      self.register_parameter('bias', None)
    self.reset_parameters()
    
    # manually set device if necessary
    self.device = 'cuda' if torch.cuda.is_available() else 'cpu' 
       
    self.coord = None

  def reset_parameters(self):
    n = self.in_channels
    for k in self.kernel_size:
        n *= k
    stdv = 1. / math.sqrt(n)
    self.weight.data.uniform_(-stdv, stdv)
    if self.bias is not None:
        self.bias.data.zero_()

  def _cache_at_first_time_run(self, h, w):
    low = - (self.kernel_size[0]//2)
    hi  = self.kernel_size[0]//2
    grid_i, grid_j = torch.meshgrid(torch.arange(low, h+hi, device=self.device),
                                        torch.arange(low, w+hi, device=self.device))
    self.coord = torch.cat((grid_i.unsqueeze(2), grid_j.unsqueeze(2)), 2) # h+2 x w+2 x 2
    
    # check out im2col procedure for more information
    self.coord = torch.as_strided(self.coord, size = (h, w, *self.kernel_size, 2),
                                  stride=(*((self.coord.stride(0), self.coord.stride(1))*2),
                                          self.coord.stride(2)) )
    self.coord = self.coord.contiguous().view(1, h, w, -1, 2).float()
    self.coord.requires_grad = False

  def forward(self, x, offset, mask): 
    # mask: B x 9 x H x W
    b, c, h, w = x.shape
    if self.coord is None:
      self._cache_at_first_time_run(h,w)
      
    offset = offset.view(b, self.kernel_size[0]**2, 2, h, w).permute([0,3,4,1,2]) # b, h, w, 9, 2
    coord = offset + self.coord
    
    coord_lt = coord.floor().long().detach() # b, h, w, 9, 2
    coord_rb = coord.ceil().long().detach()
    coord_rt = torch.stack([coord_lt[..., 0], coord_rb[..., 1]], -1)
    coord_lb = torch.stack([coord_rb[..., 0], coord_lt[..., 1]], -1)
    
    vals_lt = self._sampling(x, coord_lt.detach())
    vals_rb = self._sampling(x, coord_rb.detach())
    vals_lb = self._sampling(x, coord_lb.detach())
    vals_rt = self._sampling(x, coord_rt.detach())
    
    fract = coord - coord_lt.float()
    vals_t = self._interpolate(vals_lt, vals_rt, fract[..., 1])
    vals_b = self._interpolate(vals_lb, vals_rb, fract[..., 1])
    
    mapped_vals = self._interpolate(vals_t, vals_b, fract[..., 0])
    mapped_vals = mapped_vals.permute([1, 4, 0, 2, 3])
    mapped_vals = mapped_vals * mask.permute([1,0,2,3]).unsqueeze(0)
    mapped_vals = mapped_vals.reshape(-1, b*h*w) # C9 x BHW
    output = torch.matmul(self.weight.view(self.out_channels, -1), mapped_vals) # C' x (B x H x W)
    
    return output.view(self.out_channels, b, h, w).permute([1,0,2,3])
      
  def _sampling(self, x: torch.Tensor, coord: torch.Tensor):
    b, c, h, w = x.shape
    # coord : b, h, w, 9, 2
    k = self.kernel_size[0]**2
    coord = coord.reshape(b, 1, -1, 2).repeat(1,c,1,1).view(b*c, -1, 2)
    outside = (coord[..., 0] >= h) + (coord[..., 0] < 0) + \
              (coord[..., 1] >= w) + (coord[..., 1] < 0)
              
    indx = coord[..., 0]*w + coord[..., 1] + \
            (h*w*torch.arange(c*b, device=self.device)).view(-1, 1)
    
    x = x.view(-1).index_select(0, indx.view(-1).clamp(0, b*c*h*w-1))
    x[outside.view(-1)] = 0
    return x.reshape(b, c, h, w, k)  
    
  @staticmethod    
  def _interpolate(x: torch.Tensor, y: torch.Tensor, frac: torch.Tensor):
    '''
    Linear interpolation between x and y
    Sub-routine for bi-linear interpolation
    '''
    return x + frac*(y-x)