#!/usr/bin/kivy

import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class SpeffzKeyboard(GridLayout):
    def __init__(self, **kwargs):
        super(SpeffzKeyboard, self).__init__(**kwargs)
        self.cols = 8
        self.rows = 6
        self.letters = '  AB    ' +\
                        '  DC    ' +\
                        'EFIJMNQR' +\
                        'HGLKPOTS' +\
                        '  UV    ' +\
                        '  XW   @'

        self.add_buttons()
        self.text = ''

    def add_buttons(self):
        for i in self.letters:
            if i.isalpha():
                b = Button(text=i, background_color=self.get_color(i))
                b.bind(on_press=self.add_letter)
            elif i=="@":
                b = Button(text='<<', background_color=[1,1,1,1])
                b.bind(on_press=self.backspace)
            else:
                b = Label(text=i, background_color=[0,0,0,0])
            self.add_widget(b)

    def get_color(self, letter):
        if letter in ['A', 'B', 'C', 'D']:
            color = [1,1,1,1] # white
        elif letter in ['E', 'F', 'G', 'H']:
            color = [1,.5,0,1] # orange
        elif letter in ['I', 'J', 'K', 'L']:
            color = [0,1,0,1] # green
        elif letter in ['M', 'N', 'O', 'P']:
            color = [1,0,0,1] # red
        elif letter in ['Q', 'R', 'S', 'T']:
            color = [0,0,1,1] # blue
        elif letter in ['U', 'V', 'W', 'X']:
            color = [1,1,0,1] # yellow
        return color

    def add_letter(self, instance):
        self.text += instance.text

    def clear(self):
        self.text = ''

    def get_text(self):
        return self.text

    def backspace(self, instance):
        self.text = self.text[:-1]


class BtnSpeffzKeyboard(Button):
    def __init__(self, **kwargs):
        super(BtnSpeffzKeyboard, self).__init__(**kwargs)
        self.bind(on_press=self.callback)

    def callback(self, instance):
        content = BoxLayout(orientation='vertical')
        keyboard = SpeffzKeyboard()
        btnclose = Button(text='Close',
                            size_hint_y=None,
                            size_hint_x=1)
        content.add_widget(keyboard)
        content.add_widget(btnclose)
        popup = Popup(content=content, title='Speffs Keyboard',
                      size_hint=(1, 1),
                      auto_dismiss=False)
        btnclose.bind(on_release=popup.dismiss)
        popup.open()


class TestApp(App):
    def build(self):
        return BtnSpeffzKeyboard(text='open speffz keyboard')

if __name__ == '__main__':
    TestApp().run()
