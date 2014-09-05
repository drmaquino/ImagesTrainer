#!/usr/bin/kivy

import os
import random
import kivy
kivy.require('1.1.3')

from kivy.lang import Builder

from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import SlideTransition

from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty


CURRENT_PATH = os.path.dirname(__file__)

KV_PATH = os.path.join(CURRENT_PATH, 'images.kv')
Builder.load_file(KV_PATH)

IMAGES_PATH = os.path.join(CURRENT_PATH, '..', 'images')
image_files = os.listdir(IMAGES_PATH)

SPRITES_PATH = os.path.join(CURRENT_PATH, '..', 'sprites')
NO_IMAGE = os.path.join(SPRITES_PATH, 'black.png')
GREEN_CHECK = os.path.join(SPRITES_PATH, 'green.png')
RED_CROSS = os.path.join(SPRITES_PATH, 'red.png')


class EncodingScreen(Screen):

    filenames = ListProperty()
    current_pair = StringProperty()
    chosen_pair = StringProperty()
    current_msg = StringProperty('Touch to Start')
    current_result = StringProperty()
    already_answered = BooleanProperty(False)
    result_indicator = StringProperty(NO_IMAGE)
    PATH_IMAGE_0 = StringProperty(NO_IMAGE)
    PATH_IMAGE_1 = StringProperty(NO_IMAGE)
    PATH_IMAGE_2 = StringProperty(NO_IMAGE)
    PATH_IMAGE_3 = StringProperty(NO_IMAGE)

    def __init__(self, sm, **kwargs):
        super(EncodingScreen, self).__init__(**kwargs)
        self.sm = sm

    def start(self):
        self.reset()
        self.load_images()
        self.current_msg = 'Select the correct image'

    def load_images(self):
        self.filenames = random.sample(image_files, 4)
        self.PATH_IMAGE_0 = os.path.join(IMAGES_PATH, self.filenames[0])
        self.PATH_IMAGE_1 = os.path.join(IMAGES_PATH, self.filenames[1])
        self.PATH_IMAGE_2 = os.path.join(IMAGES_PATH, self.filenames[2])
        self.PATH_IMAGE_3 = os.path.join(IMAGES_PATH, self.filenames[3])
        self.current_pair = random.choice(self.filenames).upper()[:2]

    def register_input(self, button):
        self.chosen_pair = self.filenames[int(button.text)].upper()[:2]
        if not self.already_answered:
            self.check_result()
        self.already_answered = True
        self.current_msg = 'Click to continue...'

    def check_result(self):
        if self.chosen_pair == self.current_pair:
            self.current_result = 'Correct!'
            self.result_indicator = GREEN_CHECK
        else:
            self.current_result = 'wrong!'
            self.result_indicator = RED_CROSS

    def reset(self):
        self.filenames = []
        self.current_pair = ''
        self.chosen_pair = ''
        self.current_msg = 'Touch to Start'
        self.current_result = ''
        self.already_answered = False
        self.result_indicator = NO_IMAGE
        self.PATH_IMAGE_0 = NO_IMAGE
        self.PATH_IMAGE_1 = NO_IMAGE
        self.PATH_IMAGE_2 = NO_IMAGE
        self.PATH_IMAGE_3 = NO_IMAGE

    def quit(self):
        self.sm.transition = SlideTransition(direction='right')
        self.sm.current = 'welcome_screen'
        self.reset()