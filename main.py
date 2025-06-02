from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
import math
from kivy.graphics import Color, RoundedRectangle

Window.minimum_width = dp(400)
Window.minimum_height = dp(600)
Window.clearcolor = (0.988, 0.933, 0.890, 1)
Window.size = (int(dp(450)), int(dp(760)))



hits = 0
blunders = 0
totalNumberOfThrows = 0
PercentageOfHits = 0
switch = 0


class RoundedButton(Button):
    def __init__(self, **kwargs):
        self.radius = kwargs.pop("radius", [20])
        super(RoundedButton, self).__init__(**kwargs)
        btn_color = self.background_color
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(rgba=btn_color)
            self.rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=self.radius
            )
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class StatsScreen(Screen):
    def __init__ (self, app, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.app = app


        box = FloatLayout()


        self.labelThrows = Label(text = "THROWS", font_size = dp(75), color = (0, 0, 0, 1), font_name = "font/FranklinGothicMedium.ttf",
                            pos_hint = {"x": 0, "top": 1.3})

        self.labelTotalNumberOfThrows = Label(text = "0", font_size = dp(60), color = (0, 0, 0, 1), font_name = "font/FranklinGothicMedium.ttf",
                                         pos_hint = {"x": 0, "top": 1.2})

        labelReaction = Label(text = "estimation", font_size = dp(26), color = (0, 0, 0, 0.5), font_name = "font/FranklinGothicMedium.ttf",
                              pos_hint  = {"x": 0, "top": 1.07})

        buttonMiss = RoundedButton(text = "MISS", size_hint=(0.4, 0.15), font_name = "font/FranklinGothicMedium.ttf",
                            font_size = dp(64), color = (0.988, 0.933, 0.890, 1), radius = [5], on_press = self.plusMiss,
                            background_color = (0.56, 0.011, 0.015, 1), background_normal='',
                            pos_hint = {"x": 0.05, "top": 0.5})

        buttonHit = RoundedButton(text="HIT", size_hint=(0.4, 0.15), font_name="font/FranklinGothicMedium.ttf",
                            font_size=dp(64), color=(0.988, 0.933, 0.890, 1), radius = [5], on_press = self.plusHits,
                            background_color=(0.396, 0.553, 0.655, 1), background_normal='',
                            pos_hint={"x": 0.55, "top": 0.5})

        buttonFinish = RoundedButton(text = "FINISH", size_hint=(0.35, 0.06), font_name="font/FranklinGothicMedium.ttf",
                              font_size = dp(40), color = (0.988, 0.933, 0.890, 1), radius = [5], on_press = self.FINISH,
                              background_color = (0.5, 0.6, 0.254, 1), background_normal='',
                              pos_hint={"center_x": 0.5, "top": 0.3})

        buttonAccount = Button(size_hint=(None, None), size=(dp(70), dp(70)), border = (0, 0, 0, 0),
                               background_normal = "img/accountlogo.png", background_down = "img/accountlogo.png",
                               pos_hint = {"right": 0.98, "y": 0.01})

        buttonSwitchMusic = Button(size_hint = (None, None), size = (dp(70), dp(70)), border = (0, 0, 0, 0),
                                   background_normal = "img/musicon.png", background_down = "img/musicon.png",
                                   pos_hint = {"x": 0.02, "y": 0.01})

        buttonSwitchRight = Button(size_hint = (None, None), size = (dp(25), dp(25)), border = (0, 0, 0, 0),
                                   background_normal = "img/right.png", background_down = "img/right.png", on_press = self.SwitchRight,
                                   pos_hint = {"x": 0.87, "top": 0.815})

        buttonSwitchLeft  = Button(size_hint = (None, None), size = (dp(25), dp(25)), border = (0, 0, 0, 0),
                                   background_normal = "img/left.png", background_down = "img/left.png", on_press = self.SwitchLeft,
                                   pos_hint = {"x": 0.07, "top": 0.815})

        box.add_widget(buttonSwitchLeft)
        box.add_widget(buttonSwitchRight)
        box.add_widget(buttonSwitchMusic)
        box.add_widget(buttonAccount)
        box.add_widget(buttonFinish)
        box.add_widget(buttonHit)
        box.add_widget(buttonMiss)
        box.add_widget(labelReaction)
        box.add_widget(self.labelTotalNumberOfThrows)
        box.add_widget(self.labelThrows)
        self.add_widget(box)


    def SwitchRight(self, instance):
        global switch
        # throw = 0; hit = 1; miss = 2; percent = 3
        if switch == 0: self.labelThrows.text = "HIT"; self.labelTotalNumberOfThrows.text = str(hits); switch = 1; return
        if switch == 1: self.labelThrows.text = "MISS"; self.labelTotalNumberOfThrows.text = str(blunders); switch = 2; return
        if switch == 2: self.labelThrows.text = "PERCENT"; self.labelTotalNumberOfThrows.text = f'{str(round(PercentageOfHits))}%'; switch = 3; return
        if switch == 3: self.labelThrows.text = "THROWS"; self.labelTotalNumberOfThrows.text = str(totalNumberOfThrows); switch = 0; return

    def SwitchLeft(self, instance):
        global switch
        if switch == 0: self.labelThrows.text = "PERCENT"; self.labelTotalNumberOfThrows.text = f"{str(round(PercentageOfHits))}%"; switch = 3; return
        if switch == 3: self.labelThrows.text = "MISS"; self.labelTotalNumberOfThrows.text = str(blunders); switch = 2; return
        if switch == 2: self.labelThrows.text = "HIT"; self.labelTotalNumberOfThrows.text = str(hits); switch = 1; return
        if switch == 1: self.labelThrows.text = "THROWS"; self.labelTotalNumberOfThrows.text = str(totalNumberOfThrows); switch = 0; return

    def FINISH(self, instance):
        global PercentageOfHits
        self.app.root.current = "finish"
        finish_screen = self.app.root.get_screen("finish")
        finish_screen.labelHitsNumber.text = str(hits)
        finish_screen.labelMissNumber.text = str(blunders)
        if hits != 0 and totalNumberOfThrows != 0: PercentageOfHits = hits / totalNumberOfThrows * 100
        else: PercentageOfHits = 0
        finish_screen.labelPercentOfHitsNumber.text = f'{str(round(PercentageOfHits))}%'
        finish_screen.labelThrowsNumber.text = f'{str(totalNumberOfThrows)}'


    def plusHits(self, instance):
        global hits, totalNumberOfThrows, PercentageOfHits
        hits += 1
        totalNumberOfThrows += 1
        if hits != 0 and totalNumberOfThrows != 0: PercentageOfHits = hits / totalNumberOfThrows * 100
        if switch == 0: self.labelTotalNumberOfThrows.text = str(totalNumberOfThrows)
        if switch == 1: self.labelTotalNumberOfThrows.text = str(hits)
        if switch == 2: self.labelTotalNumberOfThrows.text = str(blunders)
        if switch == 3: self.labelTotalNumberOfThrows.text = f'{str(round(PercentageOfHits))}%'

    def plusMiss(self, instance):
        global blunders, totalNumberOfThrows
        blunders += 1
        totalNumberOfThrows += 1
        if hits != 0 and totalNumberOfThrows != 0: PercentageOfHits = hits / totalNumberOfThrows * 100
        else: PercentageOfHits = 0
        self.labelTotalNumberOfThrows.text = str(totalNumberOfThrows)
        if switch == 0: self.labelTotalNumberOfThrows.text = str(totalNumberOfThrows)
        if switch == 1: self.labelTotalNumberOfThrows.text = str(hits)
        if switch == 2: self.labelTotalNumberOfThrows.text = str(blunders)
        if switch == 3: self.labelTotalNumberOfThrows.text = f'{str(round(PercentageOfHits))}%'

class AccountScreen(Screen):
    def __init__(self, app, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)
        self.app = app






class FinishScreen(Screen):
    def __init__(self, app, **kwargs):
        super(FinishScreen, self).__init__(**kwargs)
        self.app = app

        box = FloatLayout()

        labelThrowsName = Label(text="FINISH", font_size=dp(75), color=(0, 0, 0, 1),
                            font_name="font/FranklinGothicMedium.ttf",
                            pos_hint={"x": 0, "top": 1.35})

        labelHits = Label(text="HITS", font_size = dp(45), color = (0, 0, 0, 0.5),
                          font_name = "font/FranklinGothicMedium.ttf",
                          pos_hint = {"x": 0, "top": 1.2})

        self.labelHitsNumber = Label(text = "0", font_size = dp(40), color = (0, 0, 0, 1),
                                font_name = "font/FranklinGothicMedium.ttf",
                                pos_hint = {"x": 0, "top": 1.12})

        labelMiss = Label(text="MISS", font_size=dp(45), color=(0, 0, 0, 0.5),
                          font_name="font/FranklinGothicMedium.ttf",
                          pos_hint={"x": 0, "top": 1.05})

        self.labelMissNumber = Label(text="0", font_size=dp(40), color=(0, 0, 0, 1),
                                font_name="font/FranklinGothicMedium.ttf",
                                pos_hint={"x": 0, "top": 0.98})

        labelPercentOfHits = Label(text="PERCENT OF HITS", font_size=dp(45), color=(0, 0, 0, 0.5),
                          font_name="font/FranklinGothicMedium.ttf",
                          pos_hint={"x": 0, "top": 0.91})

        self.labelPercentOfHitsNumber = Label(text="0", font_size=dp(40), color=(0, 0, 0, 1),
                                font_name="font/FranklinGothicMedium.ttf",
                                pos_hint={"x": 0, "top": 0.84})

        labelThrows = Label(text="THROWS", font_size=dp(45), color=(0, 0, 0, 0.5),
                                   font_name="font/FranklinGothicMedium.ttf",
                                   pos_hint={"x": 0, "top": 0.77})

        self.labelThrowsNumber = Label(text="0", font_size=dp(40), color=(0, 0, 0, 1),
                                         font_name="font/FranklinGothicMedium.ttf",
                                         pos_hint={"x": 0, "top": 0.7})


        buttonStart = RoundedButton(text="START", size_hint=(0.45, 0.1), font_name="font/FranklinGothicMedium.ttf",
                            font_size=dp(64), color=(0.988, 0.933, 0.890, 1), radius = [5],
                            background_color=(0.502, 0.604, 0.255, 1), background_normal='', on_press = self.START,
                            pos_hint={"center_x": 0.5 , "top": 0.16})


        box.add_widget(buttonStart)
        box.add_widget(self.labelThrowsNumber)
        box.add_widget(self.labelPercentOfHitsNumber)
        box.add_widget(labelPercentOfHits)
        box.add_widget(labelMiss)
        box.add_widget(self.labelMissNumber)
        box.add_widget(self.labelHitsNumber)
        box.add_widget(labelHits)
        box.add_widget(labelThrows)
        box.add_widget(labelThrowsName)
        self.add_widget(box)

    def START(self, instance):
        global hits, blunders, totalNumberOfThrows, PercentageOfHits
        hits = 0
        blunders = 0
        totalNumberOfThrows = 0
        PercentageOfHits = 0
        self.app.root.current = "stats"
        stats_screen = self.app.root.get_screen("stats")
        stats_screen.labelTotalNumberOfThrows.text = str(hits)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StatsScreen(app=self, name='stats'))
        sm.add_widget(AccountScreen(app=self, name='account'))
        sm.add_widget(FinishScreen(app=self, name = 'finish'))
        return sm


MyApp().run()
