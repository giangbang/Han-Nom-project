from .DB import *
from .triplet import Clustering
from PIL import Image
import numpy as np
import io

clustering = Clustering()

def str2img(image_string):
    img = Image.open(io.BytesIO(image_string))
    img = np.array(img)
    return img
    
def crop_bbox(bboxes, image):
    res = []
    for box in bboxes:
        box = np.array(box)
        xmin = np.min(box[..., 0])
        xmax = np.max(box[..., 0])
        ymin = np.min(box[..., 1])
        ymax = np.max(box[..., 1])
        res.append(image[ymin:ymax, xmin:xmax])
    return res
    
def detect_all(img_str: list):
    imgs = [str2img(img_) for img_ in img_str]
    bboxes = [detect(img) for img in imgs]
    
    predicted = []
    for i, boxes in enumerate(bboxes):
        patches = crop_bbox(boxes['bbox'], imgs[i])
        predicted.append(clustering.topk(patches, 5))
        
    return bboxes, predicted
    
