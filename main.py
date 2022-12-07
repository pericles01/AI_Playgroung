from kivy.app import App
#from kivy.factory import Factory
from kivy.properties import *
from global_components import NavigationScreenManager

class MyScreenManager(NavigationScreenManager):
    pass

class AIPlayground(App):
    manager = ObjectProperty(None)

    def build(self):
        self.manager = MyScreenManager()
        return self.manager

# Factory.register('Root', cls=Root)
# Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    AIPlayground().run()
