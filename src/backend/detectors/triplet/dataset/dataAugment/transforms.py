from typing import Tuple, Dict

import kornia
import torch
import torch.nn as nn
import torchvision.transforms as T
from PIL import Image


MEAN = (128.,)*3
STD = (128.,)*3



def augment_transforms(cfg) -> nn.Sequential:
    augs = nn.Sequential(
        kornia.augmentation.ColorJitter(.2, .2, .2, .2, p=0.6),
        kornia.augmentation.RandomBoxBlur(p=0.3),
        kornia.augmentation.RandomGaussianNoise(std=.25),
        kornia.augmentation.RandomPerspective(.3, p=.5),
        kornia.augmentation.RandomAffine(25, 0.1, scale=(0.95,1.1)),
        kornia.augmentation.RandomErasing(scale=(0.01, cfg.data.augmentation.random_erase), value=1, p=0.6),
        kornia.augmentation.RandomGrayscale(p=0.2),
        kornia.augmentation.RandomResizedCrop(
            size=[cfg.data.input_shape]*2,
            scale=(cfg.data.augmentation.resize_scale, 1.0),
            ratio=(0.75, 1.33),
            p=0.2
        ),
        # kornia.augmentation.Normalize(
            # mean=torch.tensor(MEAN),
            # std=torch.tensor(STD)
        # )
    )
    # augs = augs.to(cfg.device)
    return augs


def basic_transforms(cfg) -> T.Compose:
    return T.Compose([
        ToTensor(),
        T.Resize(size=[cfg.data.input_shape]*2),
        T.RandomApply([T.GaussianBlur(kernel_size=11, sigma=(0.1, 2.0))]),
        T.Normalize(mean=MEAN, std=STD)
    ])


def test_transforms(cfg) -> T.Compose:
    return T.Compose([
        ToTensor(),
        T.Resize(size=cfg.data.input_shape),
        T.RandomApply([T.GaussianBlur(kernel_size=5, sigma=(0.1, 2.0))]),
        Normalize(mean=MEAN, std=STD)
    ])
    
def pure_transforms(cfg) -> T.Compose:
    return T.Compose([
        ToTensor(),
        T.Resize(size=cfg.data.input_shape),
        Normalize(mean=MEAN, std=STD)
    ])
    
class Normalize(nn.Module):
    def __init__(self, mean, std):
        super().__init__()
        self.mean = torch.Tensor(mean).view(3,1,1)
        self.std = torch.Tensor(std).view(3,1,1)
        
    def forward(self, x):
        return (x-self.mean)/self.std

class ToTensor(nn.Module):
    def __init__(self):
        super().__init__()
        
    def forward(self, x):
        x = torch.Tensor(x)
        size = x.shape
        assert len(size) >= 3, size
        x = x.transpose(-1,-2).transpose(-2, -3)
        return x