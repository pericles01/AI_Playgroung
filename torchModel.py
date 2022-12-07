import os
import torch
import urllib
from urllib.request import urlopen
from urllib.error import URLError
import sys
from PIL import Image
from torchvision import transforms

class TorchModel:
    def __init__(self) -> None:
        
        self.input_batch = None
        self.accuracy = None
        self.detected_class = None
        self.model = None #torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
        self.categories = None
        self.class0 = " "
        self.class1 = " "
    
    def setup_model(self, path:str) -> None:

        try:
            self.model = torch.load(path)
            self.model.eval()
        except FileNotFoundError as e:
            print(f"File {path} not found!", file=sys.stderr)
        
        #print("successfully fetched torch model")
    
    def setup_img(self, img_path:str) -> None:

        input_image = Image.open(img_path)
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            #transforms.Normalize(mean=[0.5, 0.5, 0.5 , 0.5], std=[0.5, 0.5, 0.5, 0.5]),
        ])
        input_tensor = preprocess(input_image)
        self.input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

        #print("successfully fetched image & labels")
    
    def get_class0(self, class0:str):
        self.class0 = class0
    
    def get_class1(self, class1:str):
        self.class1 = class1

    def predict(self) -> tuple:

        url, _ = ("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt", "imagenet_classes.txt")
        try:
            with urllib.request.urlopen(url) as response:
                classes = response.read().decode('UTF-8')
                self.categories = classes.split("\n")
                #print(f"{self.categories}")
        except URLError as e:
            with open("./ressource/imagenet_classes.txt", "r") as f:
                self.categories = [s.strip() for s in f.readlines()]

        # if self.class0 and self.class1:
        #     self.categories = [str(self.class0), str(self.class1)]

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            self.input_batch = self.input_batch.to('cuda')
            self.model.to('cuda')

        with torch.no_grad():
            output = self.model(self.input_batch)
        # Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
        # print(output[0])
        # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        #print(probabilities)
        
        # Show top class for the image
        _, top_id = torch.max(output, 1)
        self.accuray = round(probabilities[top_id[0]].item(), 2)
        self.accuray *= 100
        self.detected_class = self.categories[top_id[0]]
        return self.accuray, self.detected_class