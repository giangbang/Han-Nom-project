import torch
import torch.nn as nn
from .layers import NeckLayer, Backbone, Encoder, PredictorMLP, ProjectionMLP

 
class TripletModel(nn.Module):
    def __init__(
        self,
        backbone: str,
        embedding_dim: int,
        pretrained: bool,
        freeze: bool
    ) -> None:

        super().__init__()

        # backbone network
        self.encoder = Backbone(backbone=backbone, pretrained=pretrained)

        # if freeze:
        #     for param in self.backbone.parameters():
        #         param.requires_grad = False

        self.embedding_layer = NeckLayer(self.encoder.emb_dim, embedding_dim)
        self.embedding_dim = embedding_dim

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        e = self.encoder(x)
        # print(list(e.shape))
        # print(self.encoder.emb_dim)
        return self.embedding_layer(e)


class SimSiamModel(nn.Module):

    def __init__(
        self,
        backbone: str,
        latent_dim: int,
        proj_hidden_dim: int,
        pred_hidden_dim: int,
        load_pretrained: bool
    ) -> None:

        super().__init__()

        # Encoder network
        self.encoder = Encoder(backbone=backbone, pretrained=load_pretrained)

        # Projection (mlp) network
        self.projection_mlp = ProjectionMLP(
            input_dim=self.encoder.emb_dim,
            hidden_dim=proj_hidden_dim,
            output_dim=latent_dim
        )

        # Predictor network (h)
        self.predictor_mlp = PredictorMLP(
            input_dim=latent_dim,
            hidden_dim=pred_hidden_dim,
            output_dim=latent_dim
        )
        self.embedding_dim = latent_dim

    def forward(self, x: torch.Tensor):
        return self.project(self.encode(x))

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        return self.encoder(x)

    def project(self, e: torch.Tensor) -> torch.Tensor:
        return self.projection_mlp(e)

    def predict(self, z: torch.Tensor) -> torch.Tensor:
        return self.predictor_mlp(z)

def init_simsiam_model(cfg):
    cfg.model.pretrained = False
    model = SimSiamModel(
        backbone=cfg.model.backbone,
        latent_dim=cfg.model.latent_dim,
        proj_hidden_dim=cfg.model.proj_hidden_dim,
        pred_hidden_dim=cfg.model.pred_hidden_dim,
        load_pretrained=cfg.model.pretrained,
    )
    return model
    
def init_triplet_model(cfg): 
    cfg.model.pretrained = False
    model = TripletModel(
      backbone=cfg.model.backbone,
      embedding_dim=cfg.model.embedding_dim,
      pretrained=cfg.model.pretrained,
      freeze=cfg.model.freeze
	)
    return model 