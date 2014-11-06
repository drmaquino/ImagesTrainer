#!/usr/bin/kivy

import kivy
kivy.require('1.1.3')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.welcome.welcomescreen import WelcomeScreen
from screens.encoding.encodingscreen import EncodingScreen
from screens.recall.recallscreen import RecallScreen


class ImagesApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(sm, name='welcome_screen'))
        sm.add_widget(EncodingScreen(sm, name='encoding_screen'))
        sm.add_widget(RecallScreen(sm, name='recall_screen'))
        return sm

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    ImagesApp().run()
