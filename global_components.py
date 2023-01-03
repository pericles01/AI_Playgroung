from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import *

Builder.load_file("global_components.kv")

class BoxLayoutWithActionBar(BoxLayout):
    mtitle = StringProperty()

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    file_type = OptionProperty("None", options=["model_file", "image_file", "labels_file", "None"])
    
    def apply_filters(self)-> list:
        """
        apply a specified file filtering for filechooser depending on the filetype
        see global_components.kv
        """
        if self.file_type =="image_file":
            return ["*.jpg", "*.jpeg", "*.svg", "*.png"]
        elif self.file_type =="model_file":
            return ["*.pth"] # add "*.h5" ?
        elif self.file_type =="labels_file":
            return ["*.txt"]
        else:
            return []

class NavigationScreenManager(ScreenManager):
    
    screen_stack = []

    def push(self, screen_name):
        
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.transition.direction = "left"
            self.current = screen_name

    def pop(self):
        
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.transition.direction = "right"
            self.current = screen_name