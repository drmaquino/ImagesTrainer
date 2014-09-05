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

from modules.logger import Logger


CURRENT_PATH = os.path.dirname(__file__)

KV_PATH = os.path.join(CURRENT_PATH, 'images.kv')
Builder.load_file(KV_PATH)

IMAGES_PATH = os.path.join(CURRENT_PATH, '..', 'images')
image_files = os.listdir(IMAGES_PATH)

SPRITES_PATH = os.path.join(CURRENT_PATH, '..', 'sprites')
NO_IMAGE = os.path.join(SPRITES_PATH, 'black.png')
GREEN_CHECK = os.path.join(SPRITES_PATH, 'green.png')
RED_CROSS = os.path.join(SPRITES_PATH, 'red.png')


class Data:
    def __init__(self, name='', time=0, value=0):
        self.name = name
        self.time = time
        self.value = value # 0 for Wrong, 1 for Right


class RecallScreen(Screen):
    """Manages what happens in the main window."""

    current_image = StringProperty(NO_IMAGE)
    current_pair = StringProperty()
    current_msg = StringProperty('Touch to Start')
    result_indicator = StringProperty(NO_IMAGE)
    running = BooleanProperty(False)
    correct = BooleanProperty(False)
    images = ListProperty()
    my_kb = ObjectProperty()
    my_logger = ObjectProperty()

    def __init__(self, sm, **kwargs):
        super(RecallScreen, self).__init__(**kwargs)
        self.my_logger = Logger()
        self.sm = sm

    def show_image(self):
        """Shows a random image."""
        if not self.running:
            filename = random.choice(image_files)
            self.current_pair = filename.split('.')[0]
            self.current_image = os.path.join(IMAGES_PATH, filename)
            self.current_msg = 'Submit'
            self.result_indicator = NO_IMAGE
            self.my_kb.clear()
        else:
            self.my_pair = self.my_kb.get_text()[:2]
            self.check_result()
            self.update_screen()
            self.save_to_log()
        self.running = not self.running

    def check_result(self):
        if (self.my_pair.upper() == self.current_pair.upper()):
            self.correct = True
        else:
            self.correct = False

    def update_screen(self):
        if (self.correct):
            self.result_indicator = GREEN_CHECK
            self.current_msg = 'Correct!\nThe answer is "%s"\nClick to continue...' % (self.my_pair.upper())
        else:
            self.result_indicator = RED_CROSS
            self.current_msg = 'Your Answer:  "%s"\nCorrect Answer:  "%s"\nClick to continue...' % (self.my_pair.upper(), self.current_pair.upper())

    def save_to_log(self):
        result = 0
        if (self.correct):
            result = 1
        data = Data(self.current_pair.upper(), 0, result)
        self.my_logger.add(data)
        print ("self.my_logger.get_avg()")

    def reset_data(self):
        self.current_image = NO_IMAGE
        self.result_indicator = NO_IMAGE
        self.current_pair = ''
        self.current_msg = 'Touch to Start'
        self.running = False
        self.correct = False

    def quit(self):
        self.sm.transition = SlideTransition(direction='right')
        self.sm.current = 'welcome_screen'
        self.reset_data()