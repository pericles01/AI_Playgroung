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
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    def setup_model(self, path:str) -> None:
        try:
            self.model = torch.load(path)
            self.model.eval()
            self.model.to(self.device)
        except FileNotFoundError as e:
            print(f"File {path} not found!", file=sys.stderr)

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
        self.input_batch.to(self.device)

    def predict(self) -> tuple | str:
        pass

class MultiClassModel(TorchModel):
    def __init__(self) -> None:
        super().__init__()

    def setupLabels(self, path:str)->None:
        with open(path, "r") as f:
            try:
                labels = f.read()
                self.categories = [label.strip() for label in labels.split(", ")]
            except ValueError:
                self.categories = [label.strip() for label in labels.split(",")]
            else:
                self.categories = [s.strip() for s in f.readlines()]

    def predict(self) -> tuple | str:

        if not self.categories:
            url, _ = ("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt", "imagenet_classes.txt")
            try:
                with urllib.request.urlopen(url) as response:
                    classes = response.read().decode('UTF-8')
                    self.categories = classes.split("\n")
                    #print(f"{self.categories}")
            except URLError as e:
                with open("./ressource/imagenet_classes.txt", "r") as f:
                    self.categories = [s.strip() for s in f.readlines()]

        with torch.no_grad():
            output = self.model(self.input_batch)
        # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        # Show top class for the image
        _, top_id = torch.max(output, 1)
        
        self.detected_class = self.categories[top_id[0]]
        try:
            self.accuray = round(probabilities[top_id[0]].item(), 2)
            self.accuray *= 100
            return self.accuray, self.detected_class
        except Exception:
            return 0, self.detected_class

class BinaryClassModel(TorchModel):
    def __init__(self) -> None:
        super().__init__()
        self.class0 = None
        self.class1 = None
    
    def setup_labels(self, class0:str, class1:str):
        self.class0 = class0 
        self.class1 = class1
        if "Enter class 0".lower() not in self.class0.lower() and "Enter class 1".lower() not in self.class1.lower():
            self.categories = [str(self.class0), str(self.class1)]
        else:
            self.categories = ["class 0", "class 1"]
        print(f"{self.categories}")
    
    def predict(self) -> tuple | str:

        with torch.no_grad():
            output = self.model(self.input_batch)
        # get the decision between 0 1. if output < 0.5 -> 0 else -> 1
        decision = torch.round(torch.sigmoid(output)).squeeze()
        # Show top class for the image
        _, top_id = torch.max(output, 1)
        self.detected_class = self.categories[top_id[0]] if top_id[0]< 1 else self.categories[1]
        try:
            self.accuray = round(decision[top_id[0]].item(), 2)
            self.accuray *= 100
            return self.accuray, self.detected_class
        except Exception:
            return 0, self.detected_class