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

Window.minimum_width = dp(300)
Window.minimum_height = dp(500)
Window.clearcolor = (1, 1, 1, 1)

hits = 0
blunders = 0
totalNumberOfThrows = 0
PercentageOfHits = 0
theBestTry = 0

class StatsScreen(Screen):
    def percent(self):
        global PercentageOfHits
        if totalNumberOfThrows > 0:
            PercentageOfHits = hits * 100 / totalNumberOfThrows
            self.labelPercent.text = f"Percent of hits: {str(round(PercentageOfHits))} %"
            if PercentageOfHits > 80:
                self.labelEstimation.color = (1, 0, 0, 1)
                self.labelEstimation.text = "Are you LeBron James?!"
            elif PercentageOfHits > 70:
                self.labelEstimation.color = (0.2, 0.8, 0.2, 1)
                self.labelEstimation.text = "You should go to the NBA"
            elif PercentageOfHits > 50:
                self.labelEstimation.color = (0, 0.5, 0, 1)
                self.labelEstimation.text = "Good"
            elif PercentageOfHits > 30:
                self.labelEstimation.color = (1, 0.5, 0, 1)
                self.labelEstimation.text = "Not bad"
            else:
                self.labelEstimation.color = (0.8, 0.2, 0.2, 1)
                self.labelEstimation.text = "You should practice more."

    def clickOnLabelHits(self, instance):
        global hits, totalNumberOfThrows
        totalNumberOfThrows += 1
        hits += 1
        self.labelHits.text = f"Hits: {str(hits)}"
        self.labelFullThrows.text = f"Number of throws: {str(totalNumberOfThrows)}"
        self.percent()
        self.play_sound()

    def clickOnLabelBlunders(self, instance):
        global blunders, totalNumberOfThrows
        totalNumberOfThrows += 1
        blunders += 1
        self.labelBlunders.text = f"Miss: {str(blunders)}"
        self.labelFullThrows.text = f"Number of throws: {str(totalNumberOfThrows)}"
        self.percent()
        self.play_sound()

    def clickOnReset(self, instance):
        global hits, blunders, totalNumberOfThrows, PercentageOfHits
        self.theBestTry()
        self.labelLastTry.text = f"Last attempt: {round(PercentageOfHits)}% for {totalNumberOfThrows} throws"
        hits = 0
        blunders = 0
        totalNumberOfThrows = 0
        PercentageOfHits = 0
        self.labelHits.text = f"Hits: {str(hits)}"
        self.labelFullThrows.text = f"Number of throws: {str(totalNumberOfThrows)}"
        self.labelBlunders.text = f"Miss: {str(blunders)}"
        self.labelPercent.text = f"Percent of hits: {str(round(PercentageOfHits))} %"
        self.labelEstimation.text = "estimation"
        self.labelEstimation.color = (0.5, 0.5, 0.5, 1)
        self.play_sound()

    def theBestTry(self):
        global theBestTry
        if hits > 0 and totalNumberOfThrows > 0:
            theTry = hits / totalNumberOfThrows * math.sqrt(totalNumberOfThrows)
            if theTry > theBestTry:
                theBestTry = theTry
                self.labelTheBestTry.text = f"The best attempt: {round(PercentageOfHits)}% for {totalNumberOfThrows} throws"

    def play_sound(self):
        sound = SoundLoader.load("sound/soundButton.wav")
        if sound:
            sound.play()

    def __init__(self, app, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.app = app  # Сохраняем ссылку на экземпляр приложения
        box = FloatLayout()

        logo = Image(source="img/ThreeBestt.png", size_hint=(0.5, 0.1), pos_hint={"x": 0.18, "top": 0.1})

        buttonMissed = Button(text="Miss", on_press=self.clickOnLabelBlunders, size_hint=(0.4, 0.1),
                            font_size=dp(30), pos_hint={"x": 0.05, "top": 0.7})
        buttonGot = Button(text="Hit", on_press=self.clickOnLabelHits, size_hint=(0.4, 0.1),
                         font_size=dp(30), pos_hint={"x": 0.55, "top": 0.7})
        buttonReset = Button(text="Reset", on_press=self.clickOnReset, size_hint=(0.2, 0.1),
                           font_size=dp(20), pos_hint={"x": 0.4, "top": 0.57})

        self.labelHits = Label(text="Hits: 0", font_size=dp(30), color=(0, 0, 0, 1),
                             pos_hint={"x": 0.01, "top": 0.9})
        self.labelBlunders = Label(text="Miss: 0", font_size=dp(30), color=(0, 0, 0, 1),
                                 pos_hint={"x": 0.01, "top": 0.84})
        self.labelPercent = Label(text="Percent of hits: 0%", font_size=dp(30), color=(0, 0, 0, 1),
                                pos_hint={"x": 0.01, "top": 0.78})
        self.labelFullThrows = Label(text="Number of throws: 0", font_size=dp(30), color=(0, 0, 0, 1),
                                   pos_hint={"x": 0.01, "top": 0.72})
        self.labelName = Label(text="SwishStats", font_size=dp(55), color=(0, 0, 0, 1),
                             pos_hint={"x": 0.01, "top": 1.4})
        self.labelEstimation = Label(text="estimation", font_size=dp(20), color=(0.5, 0.5, 0.5, 1),
                                   pos_hint={"x": 0.01, "top": 1.25})
        self.labelLastTry = Label(text="Last attempt: 0% for 0 throws", font_size=dp(19),
                                color=(0.5, 0.5, 0.5, 1), pos_hint={"x": 0.01, "top": 0.66})
        self.labelTheBestTry = Label(text="The best attempt: 0% for 0 throws", font_size=dp(19),
                                   color=(0.5, 0.5, 0.5, 1), pos_hint={"x": 0.01, "top": 0.62})
        buttonSwitch = Button(text="Переключение", on_press=self.toAccount, size_hint=(0.4, 0.1),
                              pos_hint={"x": 0.3, "top": 0.5})

        box.add_widget(buttonGot)
        box.add_widget(buttonMissed)
        box.add_widget(self.labelHits)
        box.add_widget(self.labelBlunders)
        box.add_widget(self.labelPercent)
        box.add_widget(self.labelFullThrows)
        box.add_widget(buttonReset)
        box.add_widget(self.labelName)
        box.add_widget(self.labelEstimation)
        box.add_widget(self.labelLastTry)
        box.add_widget(self.labelTheBestTry)
        box.add_widget(logo)
        box.add_widget(buttonSwitch)

        self.add_widget(box)

    def toAccount(self, instance):
        self.app.root.current = "account"  # Переключаем экран на AccountScreen

class AccountScreen(Screen):
    def __init__(self, app, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)
        self.app = app

        box = FloatLayout()
        label = Label(text="Это другой экран", font_size=dp(30), color = (0,0,0,1))
        buttonSwitch = Button(text="Переключение", on_press=self.toStatsScreen, size_hint=(0.4, 0.1),
                              pos_hint={"x": 0.3, "top": 0.5})
        box.add_widget(label)
        box.add_widget(buttonSwitch)
        self.add_widget(box)

    def toStatsScreen(self, instance):
        self.app.root.current = "finish"


class FinishScreen(Screen):
    def __init__(self, app, **kwargs):
        super(FinishScreen, self).__init__(**kwargs)
        self.app = app

        box = FloatLayout()
        label = Label(text="Это другой экран", font_size=dp(30), color=(0, 0, 0, 1))

        box.add_widget(label)
        self.add_widget(box)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StatsScreen(app=self, name='stats'))
        sm.add_widget(AccountScreen(app=self, name='account'))
        sm.add_widget(FinishScreen(app=self, name = 'finish'))
        return sm


MyApp().run()
