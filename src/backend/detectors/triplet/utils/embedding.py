import torch
import numpy as np

def get_embedding(cfg, model, dataset, model_name:str, name:str):
    dataloader =  torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=cfg.train.batch_size,
        shuffle=False,
        drop_last=False,
        num_workers=torch.multiprocessing.cpu_count()
    )
    try:
        return np.load(f'{model_name}_{name}_embedding.npy'), np.load(f'{model_name}_{name}_labels.npy')
    except:
        model.eval()
    
    embeddings = np.ones((len(dataset), model.embedding_dim), np.float32)
    labels = np.ones((len(dataset), 1), np.int)
    with torch.no_grad():
        img_iter = 0
        for batch, (img, label) in enumerate(dataloader):
            batch_size = img.shape[0]
            img_iter += batch_size
            img = img.to(cfg.device)
            img_embedding = model(img).cpu().numpy()
            embeddings[img_iter - batch_size: img_iter] = img_embedding
            labels[img_iter - batch_size: img_iter] = label.cpu().numpy().reshape(-1, 1)
            
        np.save('{}_{}_embedding.npy'.format(model_name, name), embeddings)
        np.save('{}_{}_labels.npy'.format(model_name, name), labels)
    return embeddings, labels