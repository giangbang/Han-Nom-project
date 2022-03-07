import torch.nn.functional as F
import torch

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self, name, fmt=':f'):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        fmtstr = '{name} {val' + self.fmt + '} ({avg' + self.fmt + '})'
        return fmtstr.format(**self.__dict__)

def calculate_std_l2_norm(z):
    """
    Calculate standard of l2 normalization
    :param z:
    :return:
    """
   # with torch.no_grad():
    z_norm = F.normalize(z.detach(), dim=1)
    return float(torch.std(z_norm, dim=1).mean().cpu())