import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import data
import math

model = nn.Sequential(
    nn.Conv2d(
        in_channels=1,
        out_channels=16,
        kernel_size=(5,5),
        stride=(2,1),
        dilation=1,
        padding="same"
    ),
    nn.Relu()
)

print(model)