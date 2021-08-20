import torch
import cv2
import numpy as np
import math
import io
from .model import *
from PIL import Image

class inference:
	image_shrt_side=736
	box_thresh=.6
	RGB_MEAN = np.array([122.67891434, 116.66876762, 104.00698793])
	
	def __init__(self):
		self.init_torch_tensor()
		self.model = SegDetectorModel(device=self.device)
		self.representer = SegDetectorRepresenter()
		self.model.load_weights()
		self.model.eval()
		
	def init_torch_tensor(self):
		# Use gpu or not
		torch.set_default_tensor_type('torch.FloatTensor')
		if torch.cuda.is_available():
			self.device = torch.device('cuda')
			torch.set_default_tensor_type('torch.cuda.FloatTensor')
		else:
			self.device = torch.device('cpu')
	
	def resize_image(self, img):
		height, width, _ = img.shape
		if height < width:
			new_height = self.image_shrt_side
			new_width = int(math.ceil(new_height / height * width / 32) * 32)
		else:
			new_width = self.image_shrt_side
			new_height = int(math.ceil(new_width / width * height / 32) * 32)
		resized_img = cv2.resize(img, (new_width, new_height))
		return resized_img


	def load_image(self, img):
		img = img.astype('float32')
		original_shape = img.shape[:2]
		img = self.resize_image(img)
		img -= self.RGB_MEAN
		img /= 255.
		img = torch.from_numpy(img).permute(2, 0, 1).float().unsqueeze(0)
		return img, original_shape
		

	def predict(self, img):
		img, original_shape = self.load_image(img)
		batch = {'shape': [original_shape]}
		with torch.no_grad():
			batch['image'] = img
			pred = self.model(img) 
			bbox, thres = self.representer.represent(batch, pred, False)
			bbox, thres = bbox[0], thres[0]
		# print(len(bbox), len(thres))
		# print(bbox.shape, thres.shape)
		bbox = bbox[thres>=self.box_thresh]
		return {
			'bbox': bbox.tolist(),
			'shape': original_shape
		}

infer = inference()

def detect_single_image(image_string):
	img = Image.open(io.BytesIO(image_string))
	img = np.array(img)
	img = infer.predict(img)
	return img