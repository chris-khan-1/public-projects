# from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.text import LabelBase

import requests
import json
from datetime import datetime, timedelta
import pandas as pd


appKey = '###########################'
HHill = "940GZZLUHOH"
Ray = "940GZZLURYL"
GPor = "940GZZLUGPS"


def get_train_df(station_code):
    getRequest = requests.get(
        f"https://api.tfl.gov.uk/Line/metropolitan/Arrivals/{station_code}?app_key={appKey}&app_id=")
    rawData = getRequest.json()

    L = []
    for i in rawData:
        x = {"Platform": i["platformName"], "Current Location": i["currentLocation"], "Destination": i["towards"],
             "Expected": i["expectedArrival"][11:19], "Est. Time to Station (m)": str(timedelta(seconds=int(i["timeToStation"])))}
        L.append(x)

    df = pd.DataFrame(L)
    df_sorted = df.sort_values(["Platform", "Expected"]).reset_index(drop=True)
    # kv_headers = [(i,dp(20)) for i in df_sorted.columns]
    return df_sorted


def get_table(station_code):
    df = get_train_df(station_code)

    newL = []
    for i in list(df.itertuples(index=False, name=None)):
        temp = []
        for j in i:
            temp.append(f"[font=DotMatrix][color=#faed2c]{j}[/color][/font]")
        newL.append(tuple(temp))

    cols = [('[font=DotMatrixBold][color=#ffffff]Platform[/color][/font]', dp(25)),
            ('[font=DotMatrixBold][color=#ffffff]Current Location[/color][/font]', dp(35)),
            ('[font=DotMatrixBold][color=#ffffff]Destination[/color][/font]', dp(35)),
            ('[font=DotMatrixBold][color=#ffffff]Expected[/color][/font]', dp(25)),
            ('[font=DotMatrixBold][color=#ffffff]Est. Time to Station (m)[/color][/font]', dp(20))]

    table = MDDataTable(
        pos_hint={'center_x': 0.5, 'center_y': 0.5},
        size_hint=(0.9, 0.6),
        rows_num=20,
        background_color="000000",
        background_color_header="000000",
        background_color_cell="#1e1915",
        background_color_selected_cell="#1e1915",
        # column_data=[(i, dp(40)) for i in df.columns],
        column_data=cols,
        row_data=newL,

    )

    return table


class MainWindow(Screen):
    def close_app(self):
        # Close the app
        MDApp.get_running_app().stop()
        pass


class RaynersLane(Screen):
    def close_app(self):
        # Close the app
        MDApp.get_running_app().stop()
        pass

    def on_enter(self):
        self.build()

    def build(self):
        try:
            self.remove_widget(self.table)
        except AttributeError:
            pass

        self.table = get_table(Ray)
        self.add_widget(self.table)
        pass

    def clear(self):
        self.remove_widget(self.table)


class HarrowHill(Screen):
    def close_app(self):
        # Close the app
        MDApp.get_running_app().stop()
        pass
    
    def on_enter(self):
        self.build()

    def build(self):
        try:
            self.remove_widget(self.table)
        except AttributeError:
            pass

        self.table = get_table(HHill)
        self.add_widget(self.table)
        pass

    def clear(self):
        self.remove_widget(self.table)


class GreatPortland(Screen):
    def close_app(self):
        # Close the app
        MDApp.get_running_app().stop()
        pass

    def on_enter(self):
        self.build()

    def build(self):
        try:
            self.remove_widget(self.table)
        except AttributeError:
            pass

        self.table = get_table(GPor)
        self.add_widget(self.table)
        pass

    def clear(self):
        self.remove_widget(self.table)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


LabelBase.register(
    name='DotMatrix', fn_regular='C:/Users/ckhan/Documents/coding_projects/tfl-api/Dot Matrix Regular.ttf')
LabelBase.register(
    name='DotMatrixBold', fn_regular='C:/Users/ckhan/Documents/coding_projects/tfl-api/Dot Matrix Bold.ttf')


class MyMainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Orange"
        return kv


if __name__ == "__main__":
    MyMainApp().run()
