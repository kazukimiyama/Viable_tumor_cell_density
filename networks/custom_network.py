import torch.nn as nn


class ConvLayer(nn.Sequential):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1,
                 groups=1):
        super(ConvLayer, self).__init__()
        self.add_module('conv', nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride,
                                          padding=padding, dilation=dilation, bias=False, groups=groups))
        self.add_module('relu', nn.LeakyReLU(inplace=True))
        self.add_module('bn', nn.BatchNorm2d(out_channels))


class ConvModel(nn.Module):
    def __init__(self, in_channels, out_channels, n_layer=3):
        super().__init__()

        channel = 32
        self.conv1 = ConvLayer(in_channels, channel, kernel_size=3, padding=1)

        self.layers = nn.Sequential()

        for i in range(n_layer):
            self.layers.add_module(f'layer{i+1}', ConvLayer(channel, channel * 2, kernel_size=3, padding=1))

        self.conv2 = ConvLayer(in_channels, channel, kernel_size=3, padding=1)

    def forward(self, x):
        out = self.conv1(x)
        out = self.layers(out)
        out = self.conv2(out)
        return out