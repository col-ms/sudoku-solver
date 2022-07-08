import torchvision
import torch.nn as nn

def get_model(model_name):
    
    if model_name == "resnet50":

        net = torchvision.models.resnet50(weights = None)

        # change first layer to use on greyscale images
        net.conv1 = nn.Conv2d(
            1, 
            64,
            kernel_size = (7, 7),
            stride = (2, 2),
            padding = (3, 3),
            bias = False
        )
        net.fc = nn.Linear(in_features = 2048, out_features = 10, bias = True)

    if model_name == "resnet101":

        net = torchvision.models.resnet101(weights = None)

        # change first layer to use on greyscale images
        net.conv1 = nn.Conv2d(
            1,
            64,
            kernel_size = (7, 7),
            stride = (2, 2),
            padding = (3, 3),
            bias = False
        )
        net.fc = nn.Linear(in_features = 2048, out_features = 10, bias = True)

    return net