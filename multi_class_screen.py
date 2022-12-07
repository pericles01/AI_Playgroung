from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import *
from kivy.lang import Builder
import os

from torchModel import TorchModel
from global_components import LoadDialog

Builder.load_file("multi_class_screen.kv")

class MultiClassRoot(FloatLayout):
    load_file_path = ObjectProperty(None)
    load_image_path = ObjectProperty(None)
    model = ObjectProperty(None)
    predict_class = StringProperty()
    predict_accuracy = NumericProperty()
    model = TorchModel()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load_file(self):
        content = LoadDialog(load=self.load_file, cancel=self.dismiss_popup, file_type="model_file")
        self._popup = Popup(title="Select a model file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    
    def show_load_image(self):
        content = LoadDialog(load=self.load_image, cancel=self.dismiss_popup, file_type="image_file")
        self._popup = Popup(title="Select a image", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_file(self, path, filename):
        
        self.load_file_path = os.path.normpath(filename[0])
        self.ids.selected_file.text = "Selected model: " + os.path.basename(self.load_file_path)
        
        self.model.setup_model(self.load_file_path)
        print(f"! Successfully fetched file: {self.load_file_path}")
        #print(f"! file choser: {filename}")
        

        self.dismiss_popup()

    def load_image(self, path, filename):
        self.load_image_path = os.path.normpath(filename[0])
        #access to cover image by id
        self.ids.image.source = self.load_image_path
        self.ids.image.reload()
        #feed the input image to the model
        self.model.setup_img(self.load_image_path)
        print(f"! Successfully fetched image: {self.load_image_path}")
        print(f"! new source image: {self.ids.image.source}")

        self.dismiss_popup()
    
    def predict(self):
        self.predict_accuracy, self.predict_class = self.model.predict()
        self.ids.class_label.text = str(self.predict_class)
        self.ids.accuracy_label.text = str(self.predict_accuracy) + "%"
        print(f"predicted class: {self.ids.class_label.text}")
        print(f"prediction accuracy: {self.ids.accuracy_label.text}")
    
    def reset(self):
        self.load_file_path = " "
        self.load_image_path = " "
        print("! reset")