#!/usr/bin/kivy

import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


class Logger:
    """Stores data and provides useful data organization features."""
    def __init__(self, datatype='elems', unit='units'):
        self.datatype=datatype
        self.unit=unit
        self.stats = {}
        self.data = []

    def add(self, data):
        self.data.append(data)
        self.count(data)

    def delete_last(self):
        if self.data != []:
            self.data.pop()
            self.update_stats()

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def reset_data(self):
        self.data = []

    def count(self, data):
        if data in self.stats:
            self.stats[data] += 1
        else:
            self.stats[data] = 1

    def get_stats(self):
        return self.stats

    def set_stats(self, stats):
        self_stats = stats

    def reset_stats(self):
        self.stats = {}

    def update_stats(self):
        self.reset_stats()
        for data in self.data:
            self.count(data)

    def get_avg(self):
        total = 0.0
        cant = 0
        for data in self.data:
            try:
                total += float(data.value)
                cant += 1
            except Exception as excp:
                print (type(excp))
                print (excp)
        if cant > 0:
            total /= cant
        else:
            total = 0.0

        return total

    def show_data(self):
        """Display a popup with stored data."""
        content = BoxLayout(orientation='vertical')
        scrollable = ScrollView(size_hint=(1, 1)) # do_scroll_x=False
        data = GridLayout(cols=1, size_hint_y=None)
        data.bind(minimum_height=data.setter('height'))
        for elem in self.data:
            line = Label(text=str(elem),
                            size_hint = (1, None),
                            height = 50)
            data.add_widget(line)
        scrollable.add_widget(data)
        content.add_widget(scrollable)

        btnclose = Button(text='Close',
                            size_hint_y=None,
                            size_hint_x=1)
        content.add_widget(btnclose)

        popup = Popup(content=content,
                      title='Total: %s %s - Avg: %.2f' % (len(self.data),
                                                        self.datatype,
                                                        self.get_avg()),
                      size_hint=(1, 1),
                      auto_dismiss=False)
        btnclose.bind(on_release=popup.dismiss)
        popup.open()


class LoggerScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoggerScreen, self).__init__(**kwargs)
        self.orientation='vertical'
        self.logger = Logger()
        self.scrollable = ScrollView(size_hint=(1, 1)) # do_scroll_x=False
        self.data = GridLayout(cols=1, size_hint_y=None)
        self.data.bind(minimum_height=self.data.setter('height'))
        self.scrollable.add_widget(self.data)
        self.add_widget(self.scrollable)

        self.btnadd = Button(text='add',
                            size_hint_y=None,
                            size_hint_x=1)
        self.btnadd.bind(on_release=self.add_data)
        self.add_widget(self.btnadd)

        self.btndelete = Button(text='delete',
                            size_hint_y=None,
                            size_hint_x=1)
        self.btndelete.bind(on_release=self.delete_data)
        self.add_widget(self.btndelete)

    def add_data(self, instance, data="test"):
        self.logger.add(data)
        self.update()
        print ("data added")

    def delete_data(self, instance):
        self.logger.delete_last()
        self.update()
        print ("data deleted")

    def update(self):
        self.data.clear_widgets()
        for elem in self.logger.data:
            line = Label(text=str(elem),
                                size_hint = (1, None),
                                height = 70)
            self.data.add_widget(line)


class BtnLogger(Button):
    def __init__(self, **kwargs):
        super(BtnLogger, self).__init__(**kwargs)
        self.bind(on_press=self.callback)

    def callback(self, instance):
        content = BoxLayout(orientation='vertical')
        logger_screen = LoggerScreen()
        btnclose = Button(text='Close',
                            size_hint_y=None,
                            size_hint_x=1)
        content.add_widget(logger_screen)
        content.add_widget(btnclose)
        popup = Popup(content=content, title='Speffs Keyboard',
                      size_hint=(1, 1),
                      auto_dismiss=False)
        btnclose.bind(on_release=popup.dismiss)
        popup.open()


class TestApp(App):
    def build(self):
        return BtnLogger(text='open logger')
        # return Logger().show_data()

if __name__ == '__main__':
    TestApp().run()
