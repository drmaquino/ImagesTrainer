#!/usr/bin/kivy

import os

from kivy.lang import Builder

from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import SlideTransition

# imports for the standalone app
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

CURRENT_PATH = os.path.dirname(__file__)

KV_PATH = os.path.join(CURRENT_PATH, 'welcomescreen.kv')
Builder.load_file(KV_PATH)


class WelcomeScreen(Screen):
    """Manages what happens in the main window."""

    def __init__(self, sm, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.sm = sm

    def open_encoding_practice(self):
        self.sm.transition = SlideTransition(direction="left")
        self.sm.current = 'encoding_screen'

    def open_recall_practice(self):
        self.sm.transition = SlideTransition(direction="left")
        self.sm.current = 'recall_screen'


class WelcomeScreenBtn(Button):
    def __init__(self, **kwargs):
        super(WelcomeScreenBtn, self).__init__(**kwargs)
        self.bind(on_press=self.callback)

    def callback(self, instance):
        content = BoxLayout(orientation='vertical')
        my_main_app = WelcomeScreen("dummy_screen_monitor")
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


class WelcomeScreenApp(App):
    def build(self):
        return WelcomeScreenBtn(text='open my app')

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    WelcomeScreenApp().run()