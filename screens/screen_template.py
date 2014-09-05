#!/usr/bin/kivy

import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.lang import Builder

Builder.load_string("""
<MyApp>:
    BoxLayout:
        orientation: 'vertical'

        Button:
            text: "wertwertert"
            pos: self.pos
        Button:
            text: "wertwertert"
        Button:
            text: "wertwertert"
    """)

class MyApp(GridLayout):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        pass

class BtnMyApp(Button):
    def __init__(self, **kwargs):
        super(BtnMyApp, self).__init__(**kwargs)
        self.bind(on_press=self.callback)

    def callback(self, instance):
        content = BoxLayout(orientation='vertical')
        my_main_app = MyApp()
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


class TestApp(App):
    def build(self):
        return BtnMyApp(text='open my app')

if __name__ == '__main__':
    TestApp().run()
