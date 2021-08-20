import os

import torch
import torch.nn as nn
import torch.nn.functional as F

from .backbones import *
from .decoders import *


class BasicModel(nn.Module):
	def __init__(self):
		nn.Module.__init__(self)
		
		self.backbone = deformable_resnet18(pretrained=False)
		self.decoder = SegDetector(**{
			"adaptive": True,
			"in_channels": [64, 128, 256, 512],
			"k": 50
		})

	def forward(self, data, *args, **kwargs):
		return self.decoder(self.backbone(data), *args, **kwargs)
				
				
class SegDetectorModel(nn.Module):
	model_path = r'./backend/detectors/DB/model/weights/final'
	
	def __init__(self, device, distributed: bool = False, local_rank: int = 0):
		super(SegDetectorModel, self).__init__()

		self.model = nn.Sequential()
		self.model.add_module("module", BasicModel())
		# for loading models       
		self.device = device
		self.to(self.device)
		

	def forward(self, data):
		data = data.to(self.device)
		pred = self.model(data)
		return pred
		
	def load_weights(self):
		states = torch.load(
				self.model_path, map_location=self.device)
		self.load_state_dict(states)