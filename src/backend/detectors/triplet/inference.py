import faiss
from .dataset.ChineseDictionary import get_allCharacters
import os
import sys
from .dataset.dataAugment import pure_transforms
from numpy import linalg as LA
import numpy as np
from .models import *
from .utils import preprocess_img

class Clustering:
    def __init__(self, embedding_path='font_embedding/font_embedding.npy'):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.embedding_path = os.path.join(dir_path, embedding_path)
        print('Loading font embedding...')
        with open(self.embedding_path, 'rb') as f:
            self.embedding = np.load(f)
        print('Done')
        assert len(self.embedding.shape) == 2
        self.faiss_index = faiss.IndexFlatL2(self.embedding.shape[-1])
        self.faiss_index.add(self.embedding)
        self.allCharacters = get_allCharacters()
        assert len(self.allCharacters) == len(self.embedding)
        
        from .utils import parse_args

        cfg_path = os.path.join(dir_path, 'experiment_configs/train_triplet.yaml')
        cfg = parse_args(cfg_path)
        cfg.device = 'cpu'
        

        self.model = init_triplet_model(cfg)
        model_path = os.path.join(dir_path, 'weights/mixed_finetune_final.pt')
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.to(cfg.device)
        self.model.eval()
        
        self.transform = pure_transforms(cfg)
        self.cfg = cfg
        
            
    def topk(self, query_images, k):
        # preprocessing: resize, grayscale etc
        images = []
        for img in query_images:
            processed_img = np.array(img)
            processed_img = np.array(preprocess_img(processed_img, self.cfg.data.input_shape))
            processed_img = self.transform(processed_img).unsqueeze(0)
            images.append(processed_img)
        images = torch.cat(images).to(self.cfg.device)
        
        # embed 
        with torch.no_grad():
            query_embedding = self.model(images).cpu().numpy()
            
        query_embedding = query_embedding / LA.norm(query_embedding, 
            axis=-1, keepdims=True)
        
        # top k
        _, I = self.faiss_index.search(query_embedding, k)
        
        # convert to string characters
        predicted_strs = []
        for i in I:
            predicted_strs.append([self.allCharacters[j] for j in i])
        return predicted_strs
        
        