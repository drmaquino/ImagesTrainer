from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import SlideTransition

from modules.logger import Logger


class WelcomeScreen(Screen):

    def __init__(self, sm, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.my_logger = Logger()
        self.sm = sm

    def open_encoding_practice(self):
        self.sm.transition = SlideTransition(direction="left")
        self.sm.current = 'encoding_screen'

    def open_recall_practice(self):
        self.sm.transition = SlideTransition(direction="left")
        self.sm.current = 'recall_screen'