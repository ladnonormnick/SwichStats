from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from datetime import date
from kivy.config import Config


Window.minimum_width = dp(360)
Window.minimum_height = dp(740)
Window.clearcolor = (0.988, 0.933, 0.890, 1)
Window.size = (dp(360), dp(740))

hits = 0
blunders = 0
totalNumberOfThrows = 0
PercentageOfHits = 0
switch = 0
soundOn = 0
Animation = 0
today = date.today()

date_exists = False
try:
    with open("info.txt", "r") as file:
        for line in file:
            if "timecreate" in line:
                date_exists = True
                print("дата уже есть")
                break
    if not date_exists:
        with open("info.txt", "a") as file:  # Используем 'a' для добавления
            file.write(f"timecreate = {today}\n")
except FileNotFoundError:
    with open("info.txt", "w") as file:
        file.write(f"timecreate = {today}\n")


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


        self.labelThrows = Label(text = "THROWS", font_size = dp(70), color = (0, 0, 0, 1), font_name = "font/FranklinGothicMedium.ttf",
                            pos_hint = {"x": 0, "y": 0.3})

        self.labelTotalNumberOfThrows = Label(text = "0", font_size = dp(60), color = (0, 0, 0, 1), font_name = "font/FranklinGothicMedium.ttf",
                                         pos_hint = {"x": 0, "top": 1.2})

        labelReaction = Label(text = "SWICHSTATS", font_size = dp(26), color = (0, 0, 0, 0.5), font_name = "font/FranklinGothicMedium.ttf",
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

        self.buttonAccount = Button(size_hint=(None, None), size=(dp(70), dp(70)), border = (0, 0, 0, 0),
                               background_normal = "img/accountlogo.png", background_down = "img/accountlogo.png", on_press = self.ACCOUNT,
                               pos_hint = {"right": 0.98, "y": 0.01})

        self.buttonSwitchMusic = Button(size_hint = (None, None), size = (dp(70), dp(70)), border = (0, 0, 0, 0),
                                   background_normal = "img/musicon.png", background_down = "img/musicon.png", on_press = self.SwitchSound,
                                   pos_hint = {"x": 0.02, "y": 0.01})

        buttonSwitchRight = Button(size_hint = (None, None), size = (dp(25), dp(25)), border = (0, 0, 0, 0),
                                   background_normal = "img/right.png", background_down = "img/right.png", on_press = self.SwitchRight,
                                   pos_hint = {"x": 0.89, "top": 0.815})

        buttonSwitchLeft  = Button(size_hint = (None, None), size = (dp(25), dp(25)), border = (0, 0, 0, 0),
                                   background_normal = "img/left.png", background_down = "img/left.png", on_press = self.SwitchLeft,
                                   pos_hint = {"x": 0.04, "top": 0.815})

        box.add_widget(buttonSwitchLeft)
        box.add_widget(buttonSwitchRight)
        box.add_widget(self.buttonSwitchMusic)
        box.add_widget(self.buttonAccount)
        box.add_widget(buttonFinish)
        box.add_widget(buttonHit)
        box.add_widget(buttonMiss)
        box.add_widget(labelReaction)
        box.add_widget(self.labelTotalNumberOfThrows)
        box.add_widget(self.labelThrows)
        self.add_widget(box)


    def soundClick(self, instance):
        global soundOn
        sound = SoundLoader.load("sound/soundButton.wav")
        if soundOn == 0: sound.play()
        if soundOn == 2: sound.play(); soundOn = 0

    def SwitchSound(self, instance):
        global soundOn
        print(soundOn)
        self.soundClick(instance)
        if soundOn == 0: self.buttonSwitchMusic.background_normal = "img/musicoff.png"; soundOn = 1; return
        if soundOn == 1: self.buttonSwitchMusic.background_normal = "img/musicon.png"; soundOn = 2; self.soundClick(instance); return

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
        self.soundClick(instance)

    def ACCOUNT(self, instance):
        import os
        self.app.root.current = "account"
        self.soundClick(instance)
        self.buttonAccount.size = (dp(80), dp(80))
        try:
            with open("info.txt", 'r') as file:
                for line in file:
                    if line.startswith("allthrows ="):
                        value = line.split("=")[1].strip()
                        print (f"{value} тут")
                        account_screen = self.app.root.get_screen("account")
                        account_screen.Throws.text = value

        except FileNotFoundError: print("не");

        try:
            with open("info.txt", 'r') as file:
                for line in file:
                    if line.startswith("procentfull ="):
                        value = line.split("=")[1].strip()
                        print (f"{value} тут")
                        account_screen = self.app.root.get_screen("account")
                        account_screen.HITPER.text = f"{value}%"

        except FileNotFoundError: print("не");

        try:
            with open("info.txt", 'r') as file:
                for line in file:
                    if line.startswith("timecreate ="):
                        value = line.split("=")[1].strip()
                        print (f"{value} тут")
                        account_screen = self.app.root.get_screen("account")
                        account_screen.DateOfCreation.text = value

        except FileNotFoundError: print("не");

    def plusHits(self, instance):
        global hits, totalNumberOfThrows, PercentageOfHits
        hits += 1
        totalNumberOfThrows += 1
        self.soundClick(instance)
        if hits != 0 and totalNumberOfThrows != 0: PercentageOfHits = hits / totalNumberOfThrows * 100
        if switch == 0: self.labelTotalNumberOfThrows.text = str(totalNumberOfThrows)
        if switch == 1: self.labelTotalNumberOfThrows.text = str(hits)
        if switch == 2: self.labelTotalNumberOfThrows.text = str(blunders)
        if switch == 3: self.labelTotalNumberOfThrows.text = f'{str(round(PercentageOfHits))}%'
        self.checkinfo()
        self.checkinfoPlus()

    def checkinfo(self):
        variable_name = "allthrows"
        try:
            with open("info.txt", 'r') as file:
                content = file.readlines()
        except FileNotFoundError:
            content = []

        updated = False
        new_content = []

        # Обновляем allthrows
        for line in content:
            if variable_name in line:
                try:
                    current_value = int(line.split('=')[1].strip())
                    current_value += 1
                    new_content.append(f"{variable_name} = {current_value}\n")
                    print(f"Переменная {variable_name} обновлена")
                    updated = True
                except (IndexError, ValueError):
                    new_content.append(line)
            else:
                new_content.append(line)

        if not updated and not any(variable_name in line for line in content):
            new_content.append(f"{variable_name} = {totalNumberOfThrows}\n")
            print(f"Переменная {variable_name} добавлена")
            updated = True

        # Добавляем/обновляем процент
        hits_value = 0
        allthrows_value = 0

        for line in new_content:
            if "hits =" in line:
                hits_value = int(line.split('=')[1].strip())
            if "allthrows =" in line:
                allthrows_value = int(line.split('=')[1].strip())

        if allthrows_value > 0:
            procent = (hits_value / allthrows_value) * 100
        else:
            procent = 0

        # Удаляем старую запись процента если есть
        new_content = [line for line in new_content if not line.startswith("procentfull =")]
        new_content.append(f"procentfull = {round(procent)}\n")

        # Записываем всё обратно
        with open("info.txt", 'w') as file:
            file.writelines(new_content)

    def checkinfoPlus(self):
        variable_name = "hits"
        try:
            with open("info.txt", 'r') as file:
                content = file.readlines()
        except FileNotFoundError:
            content = []

        updated = False
        new_content = []

        for line in content:
            if variable_name in line:
                try:
                    current_value = int(line.split('=')[1].strip())
                    current_value += 1
                    new_content.append(f"{variable_name} = {current_value}\n")
                    print(f"Переменная {variable_name} обновлена")
                    updated = True
                except (IndexError, ValueError):
                    new_content.append(line)
            else:
                new_content.append(line)

        if not updated and not any(variable_name in line for line in content):
            new_content.append(f"{variable_name} = 1\n")
            print(f"Переменная {variable_name} добавлена")
            updated = True

        if updated:
            with open("info.txt", 'w') as file:
                file.writelines(new_content)


    def plusMiss(self, instance):
        global blunders, totalNumberOfThrows, PercentageOfHits
        blunders += 1
        totalNumberOfThrows += 1
        self.soundClick(instance)
        if hits != 0 and totalNumberOfThrows != 0: PercentageOfHits = hits / totalNumberOfThrows * 100
        else: PercentageOfHits = 0
        self.labelTotalNumberOfThrows.text = str(totalNumberOfThrows)
        if switch == 0: self.labelTotalNumberOfThrows.text = str(totalNumberOfThrows)
        if switch == 1: self.labelTotalNumberOfThrows.text = str(hits)
        if switch == 2: self.labelTotalNumberOfThrows.text = str(blunders)
        if switch == 3: self.labelTotalNumberOfThrows.text = f'{str(round(PercentageOfHits))}%'
        self.checkinfo()

class AccountScreen(Screen):
    def __init__(self, app, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)
        self.app = app

        box = FloatLayout()

        UserLabel = RoundedButton(text = "USER", size_hint=(0.6, 0.09), font_name="font/FranklinGothicMedium.ttf",
                              font_size = dp(60), color = (0, 0, 0, 1), radius = [10],
                              background_color = (210/255, 211/255, 213/255, 1), background_normal='',
                              pos_hint={"center_x": 0.5, "top": 0.62})

        UserLogo = Image(source="img/userlogo.png", size_hint=(None, None), size=(dp(250), dp(250)),
                         pos_hint={"center_x": 0.5, "top": 0.97})

        LabelTHROWS = Label(text = "ALLTIME THROWS", font_name = "font/FranklinGothicMedium.ttf",
                            font_size = dp(35), color = (0, 0, 0, 1),
                            pos_hint = {"center_x": 0.5, "top": 0.97})

        self.Throws = RoundedButton(text="0", size_hint=(0.55, 0.09), font_name="font/FranklinGothicMedium.ttf",
                                  font_size=dp(35), color=(0, 0, 0, 1), radius=[10],
                                  background_color=(210 / 255, 211 / 255, 213 / 255, 1), background_normal='',
                                  pos_hint={"x": 0.03, "top": 0.43})

        Blue = RoundedButton(size_hint=(0.37, 0.09), background_color=(0.3961, 0.5529, 0.6549, 1), background_normal = "", radius = [10],
                             pos_hint = {"x": 0.6, "top": 0.43})

        Date = Label(text = "DATE OF CREATION", font_name = "font/FranklinGothicMedium.ttf",
                            font_size = dp(35), color = (0, 0, 0, 1),
                            pos_hint = {"center_x": 0.5, "top": 0.8})

        self.DateOfCreation = RoundedButton(text="2023-10-01", size_hint=(0.7, 0.09,), font_name="font/FranklinGothicMedium.ttf",
                                font_size=dp(35), color=(0, 0, 0, 1), radius=[10],
                                  background_color=(210 / 255, 211 / 255, 213 / 255, 1), background_normal='',
                                  pos_hint={"x": 0.27, "top": 0.26})

        Red = RoundedButton(size_hint=(0.22, 0.09), background_color=(0.5608, 0.0118, 0.0157, 1), background_normal = "", radius = [10],
                             pos_hint = {"x": 0.03, "top": 0.26})

        HIT = Label(text="HIT PERCENTAGE", font_name="font/FranklinGothicMedium.ttf",
                     font_size=dp(35), color=(0, 0, 0, 1),
                     pos_hint={"center_x": 0.5, "top": 0.63})

        self.HITPER = RoundedButton(text="0%", size_hint=(0.4, 0.09,),
                                       font_name="font/FranklinGothicMedium.ttf",
                                       font_size=dp(35), color=(0, 0, 0, 1), radius=[10],
                                       background_color=(210 / 255, 211 / 255, 213 / 255, 1), background_normal='',
                                       pos_hint={"x": 0.03, "top": 0.1})

        GREEN = RoundedButton(size_hint=(0.52, 0.09), background_color=(0.50196, 0.60392, 0.25490, 1), background_normal="",
                            radius=[10],
                            pos_hint={"x": 0.45, "top": 0.1})

        butttonBack = Button(size_hint = (None, None), size = (dp(60), dp(60)), border = (0, 0, 0, 0),
                                   background_normal = "img/back.png", background_down = "img/back.png", on_press = self.BACK,
                                   pos_hint = {"x": 0.01, "center_y": 0.95})



        box.add_widget(butttonBack)
        box.add_widget(GREEN)
        box.add_widget(self.HITPER)
        box.add_widget(HIT)
        box.add_widget(Red)
        box.add_widget(Date)
        box.add_widget(self.DateOfCreation)
        box.add_widget(Blue)
        box.add_widget(self.Throws)
        box.add_widget(LabelTHROWS)
        box.add_widget(UserLabel)
        box.add_widget(UserLogo)
        self.add_widget(box)

    def BACK(self, instance):
        self.app.root.current = "stats"
        stats_screen = self.app.root.get_screen("stats")
        stats_screen.soundClick(instance)
        stats_screen.buttonAccount.size = (dp(70), dp(70))

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
                            font_size=dp(55), color=(0.988, 0.933, 0.890, 1), radius = [5],
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
        stats_screen.soundClick(instance)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StatsScreen(app=self, name='stats'))
        sm.add_widget(AccountScreen(app=self, name='account'))
        sm.add_widget(FinishScreen(app=self, name = 'finish'))
        return sm


MyApp().run()
