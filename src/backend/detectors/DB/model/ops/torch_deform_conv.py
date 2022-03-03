import torchvision
import torch

class ModulatedDeformConv(torchvision.ops.deform_conv.DeformConv2d):
    def __init__(self,
        in_channels: int,
        out_channels: int,
        kernel_size: 3,
        stride: int = 1,
        padding: int = 1,
        dilation: int = 1,
        groups: int = 1,
        deformable_groups=1,
        bias: bool = False,):
        
        super().__init__(in_channels,
        out_channels,
        kernel_size,
        stride,
        padding,
        dilation,
        groups,
        bias)
        