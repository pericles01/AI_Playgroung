import os
import torch
import urllib
from urllib.request import urlopen
from PIL import Image

if __name__ == '__main__':

    path = "./resnet18.pth"
    # model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
    # torch.save(model, path)
    # print(f"successfully saved torch resnet model")
    model = torch.load(path)
    print(f"successfully loaded {path}")
    url, filename = ("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt", "imagenet_classes.txt")
    # try: urllib.URLopener().retrieve(url, filename)
    # except: urllib.request.urlretrieve(url, filename)
    # with open("imagenet_classes.txt", "r") as f:
    #     categories = [s.strip() for s in f.readlines()]
    #     print(f"{categories}")

    # with urllib.request.urlopen(url) as response:
    #     classes = response.read().decode('UTF-8')
    #     categories = classes.split("\n")
    #     print(f"{categories}")