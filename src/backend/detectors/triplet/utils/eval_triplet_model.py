import torch
from pytorch_metric_learning import testers
from tqdm.auto import tqdm
import numpy as np
import torch.nn.functional as F
from PIL import Image
import json
import argparse
from types import SimpleNamespace


# convenient function from pytorch-metric-learning ###
def get_all_embeddings(dataset, model):
    tester = testers.BaseTester()
    return tester.get_all_embeddings(dataset, model)


# compute accuracy using AccuracyCalculator from pytorch-metric-learning ###
def eval_metric_model(query_set, eval_set, model, accuracy_calculator, writer, n_iter):
    query_embeddings, query_labels = get_all_embeddings(query_set, model)
    eval_embeddings, eval_labels = get_all_embeddings(eval_set, model)
    query_labels = query_labels.squeeze(1)
    eval_labels = eval_labels.squeeze(1)
    print("Computing accuracy")
    accuracies = accuracy_calculator.get_accuracy(
        query_embeddings, eval_embeddings, query_labels, eval_labels, False
    )
    writer.add_scalar("eval/acc", scalar_value=float(accuracies["precision_at_1"]), global_step=n_iter)
    writer.add_scalar("eval/mAP", scalar_value=float(accuracies['mean_average_precision']),
                      global_step=n_iter)
    writer.add_scalar("eval/r_precision", scalar_value=float(accuracies['r_precision']), global_step=n_iter)
    writer.add_scalar("eval/mean_average_precision_at_r",
                      scalar_value=float(accuracies['mean_average_precision_at_r']), global_step=n_iter)
    model.train()

    print("Test set accuracy (Precision@1) = {}".format(accuracies["precision_at_1"]))
    print(f"Test MAP: {accuracies['mean_average_precision']}")
    print(f"Test r_Precision: {accuracies['r_precision']}")
    print(f"Test mean_average_precision_at_r: {accuracies['mean_average_precision_at_r']}")
    
    return accuracies