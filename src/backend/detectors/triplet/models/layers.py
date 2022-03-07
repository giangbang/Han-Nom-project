from torch import nn
import torch
import torch.nn.functional as F
import torchvision
import timm


class GeM(nn.Module):
    def __init__(self, p=3, eps=1e-6):
        super(GeM, self).__init__()
        self.p = nn.Parameter(torch.ones(1) * p)
        self.eps = eps

    def forward(self, x):
        return self.gem(x, p=self.p, eps=self.eps)

    def gem(self, x, p=3, eps=1e-6):
        return F.avg_pool2d(x.clamp(min=eps).pow(p), (x.size(-2), x.size(-1))).pow(1. / p)

    def __repr__(self):
        return self.__class__.__name__ + '(' + 'p=' + '{:.4f}'.format(self.p.data.tolist()[0]) + ', ' + 'eps=' + str(
            self.eps) + ')'


class Backbone(nn.Module):

    def __init__(
        self,
        backbone: str,
        pretrained: bool
    ):
        super().__init__()
        self.model = timm.create_model(backbone, pretrained=pretrained, num_classes=0, global_pool='')
        self.emb_dim = self.model.num_features  # depend on model to get right embedding dim

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)


class NeckLayer(nn.Module):
    def __init__(
        self,
        input_dim: int,
        embedding_dim: int,
    ) -> None:
        super().__init__()
        self.GeM = GeM()
        self.model = nn.Sequential(
            nn.Linear(input_dim, embedding_dim),
            nn.BatchNorm1d(embedding_dim),
            nn.PReLU()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.GeM(x)
        x = x.squeeze(-1).squeeze(-1)
        return self.model(x)


class Encoder(nn.Module):

    def __init__(
        self,
        backbone: str,
        pretrained: bool
    ):
        super().__init__()
        model = getattr(torchvision.models, backbone)(pretrained=pretrained)
        self.emb_dim = model.fc.in_features  # change to get embedding_dim
        self.model = nn.Sequential(*list(model.children())[:-1])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x).squeeze()


class PredictorMLP(nn.Module):

    def __init__(
            self,
            input_dim: int,
            hidden_dim: int,
            output_dim: int
    ) -> None:
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)


class ProjectionMLP(nn.Module):

    def __init__(
            self,
            input_dim: int,
            hidden_dim: int,
            output_dim: int
    ) -> None:
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, output_dim),
            nn.BatchNorm1d(output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)