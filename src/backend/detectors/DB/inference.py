import torch
import cv2
import numpy as np
import math
import io
from .model import *
from PIL import Image

class DBInference:
    image_shrt_side=736
    box_thresh=.6
    RGB_MEAN = np.array([122.67891434, 116.66876762, 104.00698793])
    
    def __init__(self):
        self.init_torch_tensor()
        self.model = SegDetectorModel(device=self.device)
        self.representer = SegDetectorRepresenter()
        print('Loading model...')
        self.model.load_weights()
        print('Done.')
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

    def str2img(self, image_string):
        img = Image.open(io.BytesIO(image_string))
        img = np.array(img)
        return img

    def detect_single_image(self, image_string):
        '''
        Detect bounding boxes of a single image, the input image is in string format
        '''
        img = self.str2img(image_string)
        img = self.predict(img)
        return img
        
    def detect_batch_image(self, image_batch_string):
        '''
        Batch version of `detect_single_image`
        `image_batch_string` is a list of string image
        '''
        _imgs = [self.str2img(img_str) for img_str in image_batch_string]
        
        _imgs = [self.load_image(_img) for _img in _imgs]
        
        _imgs, _img_shapes = list(zip(*_imgs))
        
        _img_shapes = list(_img_shapes)
    
        _imgs = torch.cat(_imgs)
        
        batch = {'image': _imgs, 'shape': _img_shapes}
        
        with torch.no_grad():
            pred = self.model(_imgs)
            bbox, thres = self.representer.represent(batch, pred, False)
        bbox = [bbox[i][thres[i]>=self.box_thresh].tolist() for i in range(len(bbox))]
        return {
            'bbox': bbox,
            'shape': _img_shapes
        }
        
infer = DBInference()

def detect_single_image(image_string):
    return infer.detect_single_image(image_string)
    
def detect_batch_image(image_batch_string):
    return infer.detect_batch_image(image_batch_string)