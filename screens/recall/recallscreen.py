#!/usr/bin/kivy

import os
import random
import kivy
kivy.require('1.1.3')

from kivy.lang import Builder

from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty

from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import SlideTransition

from kivy.clock import Clock

# imports for the standalone app
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from speffzkeyboard import SpeffzKeyboard

CURRENT_PATH = os.path.dirname(__file__)

KV_PATH = os.path.join(CURRENT_PATH, 'recallscreen.kv')
Builder.load_file(KV_PATH)

IMAGES_PATH = os.path.join(CURRENT_PATH, '..', '..', 'images')
image_files = os.listdir(IMAGES_PATH)

SPRITES_PATH = os.path.join(CURRENT_PATH, '..', '..', 'sprites')
NO_IMAGE = os.path.join(SPRITES_PATH, 'black.png')
GREEN_CHECK = os.path.join(SPRITES_PATH, 'green.png')
RED_CROSS = os.path.join(SPRITES_PATH, 'red.png')


class RecallScreen(Screen):
    """Decode letter pairs from images."""

    current_image = StringProperty(NO_IMAGE)
    current_pair = StringProperty()
    current_msg = StringProperty('Touch to Start')
    result_indicator = StringProperty(NO_IMAGE)
    running = BooleanProperty(False)
    correct = BooleanProperty(False)
    images = ListProperty()
    my_kb = ObjectProperty()
    my_pair = StringProperty()

    def __init__(self, sm, **kwargs):
        super(RecallScreen, self).__init__(**kwargs)
        self.sm = sm

    def update_my_pair(self,dt):
        self.my_pair = self.my_kb.get_text()

    def main_action(self):
        """Main button. Actions depends on game state."""
        if not self.running:
            self.show_images()
            Clock.schedule_interval(self.update_my_pair, 0.1)
        else:
            self.check_result()
            Clock.unschedule(self.update_my_pair)
        self.running = not self.running

    def show_images(self):
        """Shows a random image."""
        filename = random.choice(image_files)
        self.current_pair = filename.split('.')[0]
        self.current_image = os.path.join(IMAGES_PATH, filename)
        self.current_msg = 'Submit'
        self.result_indicator = NO_IMAGE
        self.my_kb.clear()

    def check_result(self):
        if (self.my_pair.upper() == self.current_pair.upper()):
            self.result_indicator = GREEN_CHECK
            self.current_msg = 'Correct!\nClick to continue...'
        else:
            self.result_indicator = RED_CROSS
            self.current_msg = 'Correct Answer:  "%s"\nClick to continue...' % (self.current_pair.upper())

    def reset(self):
        self.current_image = NO_IMAGE
        self.result_indicator = NO_IMAGE
        self.current_pair = ''
        self.my_pair = ''
        self.current_msg = 'Touch to Start'
        self.running = False
        self.correct = False

    def quit(self):
        self.reset()
        try:
            Clock.unschedule(self.update_my_pair)
        except:
            print('nothing to unschedule')
        try:
            self.sm.transition = SlideTransition(direction='right')
            self.sm.current = 'welcome_screen'
        except:
            print('no se utilizo un screen manager')


class RecallScreenBtn(Button):
    def __init__(self, **kwargs):
        super(RecallScreenBtn, self).__init__(**kwargs)
        self.bind(on_press=self.callback)

    def callback(self, instance):
        content = BoxLayout(orientation='vertical')
        my_main_app = RecallScreen("dummy_screen_monitor")
        btnclose = Button(text='Close',
                            size_hint_y=None,
                            size_hint_x=1)
        content.add_widget(my_main_app)
        content.add_widget(btnclose)
        popup = Popup(content=content, title='my app',
                      size_hint=(1, 1),
                      auto_dismiss=False)
        btnclose.bind(on_release=popup.dismiss)
        popup.open()


class RecallScreenApp(App):
    def build(self):
        return RecallScreenBtn(text='open my app')

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    RecallScreenApp().run()
