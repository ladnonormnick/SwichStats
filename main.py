from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Ellipse
import math
from kivy.uix.image import Image


Window.minimum_width = dp(300)
Window.minimum_height = dp(500)
Window.clearcolor = (1, 1, 1, 1)



hits = 0
blunders = 0
totalNumberOfThrows = 0
PercentageOfHits = 0
theBestTry = 0


class Application(App):



    def percent(self):
        global PercentageOfHits
        PercentageOfHits = hits * 100 / totalNumberOfThrows
        self.labelPercent.text = f"Percent of hits: {str(round(PercentageOfHits))} %"
        if PercentageOfHits > 30:
            self.labelEstimation.color = (1, 0.5, 0, 1)
            self.labelEstimation.text = ("Not bad")
        if PercentageOfHits > 50:
            self.labelEstimation.color = (0, 0.5, 0, 1)
            self.labelEstimation.text = ("Good")
        if PercentageOfHits > 70:
            self.labelEstimation.color = (0.2, 0.8, 0.2, 1)
            self.labelEstimation.text = ("You should go to the NBA")
        if PercentageOfHits > 80:
            self.labelEstimation.color = (1, 0, 0, 1)
            self.labelEstimation.text = ("Are you LeBron James?!")
        if PercentageOfHits <= 30:
            self.labelEstimation.color = (0.8, 0.2, 0.2, 1)
            self.labelEstimation.text = ("You should practice more.")

    def clickOnLabelHits(self, instance):
        global hits
        global totalNumberOfThrows
        totalNumberOfThrows += 1
        hits += 1
        self.labelHits.text = f"Hits: {str(hits)}"
        self.labelFullThrows.text = f"Number of hits: {str(totalNumberOfThrows)}"
        self.percent()
        self.play_sound()

    def clickOnLabelBlunders(self, instance):
        global blunders
        global totalNumberOfThrows
        totalNumberOfThrows += 1
        blunders += 1
        self.labelBlunders.text = f"Miss: {str(blunders)}"
        self.labelFullThrows.text = f"Number of hits: {str(totalNumberOfThrows)}"
        self.percent()
        self.play_sound()

    def clickOnReset(self, instance):
        global hits
        global blunders
        global totalNumberOfThrows
        global PercentageOfHits
        self.theBestTry()
        self.labelLastTry.text = f"Last attempt: {round(PercentageOfHits)}% for {totalNumberOfThrows} throws"
        hits = 0
        blunders = 0
        totalNumberOfThrows = 0
        PercentageOfHits = 0
        self.labelHits.text = f"Hits: {str(hits)}"
        self.labelFullThrows.text = f"Number of hits: {str(totalNumberOfThrows)}"
        self.labelBlunders.text = f"Miss: {str(blunders)}"
        self.labelPercent.text = f"Percent of hits: {str(round(PercentageOfHits))} %"
        self.labelEstimation.text="estimation"
        self.labelEstimation.color=(0.5, 0.5, 0.5, 1)
        self.play_sound()


    def theBestTry(self):
        global theBestTry
        if hits > 0 and totalNumberOfThrows > 0:
            theTry = hits / totalNumberOfThrows * math.sqrt(totalNumberOfThrows)
            if theTry > theBestTry:
                theBestTry = theTry
                self.labelTheBestTry.text= f"The best attempt: {round(PercentageOfHits)}% for {totalNumberOfThrows} throws"

        else:
            print("ошибка")


    def play_sound(self):
        sound = SoundLoader.load("sound/soundButton.wav")
        sound.play()



    def build(self):


        Box = FloatLayout()


        logo = Image(source = "img/ThreeBestt.png", size_hint=(0.5,0.1),pos_hint = {"x": 0.18, "top": 0.1})

        buttonMissed = Button(text = "Miss", on_press = self.clickOnLabelBlunders,size_hint = (0.4, 0.1),font_size = dp(30), pos_hint = {"x": 0.05, "top": 0.7})
        buttonGot = Button(text = "Hit", on_press = self.clickOnLabelHits, size_hint = (0.4, 0.1),font_size = dp(30), pos_hint = {"x": 0.55, "top": 0.7})
        buttonReset = Button(text = "Reset", on_press = self.clickOnReset, size_hint = (0.2, 0.1),font_size = dp(20), pos_hint = {"x": 0.4, "top": 0.57})

        self.labelHits = Label(text = "Hits: 0", font_size = dp(30), color = (0, 0, 0, 1), pos_hint = {"x": 0.01, "top": 0.9})
        self.labelBlunders = Label(text = "Miss: 0", font_size = dp(30), color = (0, 0, 0, 1), pos_hint = {"x": 0.01, "top": 0.84})
        self.labelPercent = Label (text = "Percent of hits: 0%", font_size = dp(30), color = (0, 0, 0, 1), pos_hint = {"x": 0.01, "top": 0.78})
        self.labelFullThrows = Label (text = "Number of hits: 0", font_size = dp(30), color = (0, 0, 0, 1), pos_hint = {"x": 0.01, "top": 0.72})
        self.labelName = Label (text = "SwishStats", font_size = dp(55), color = (0, 0, 0, 1), pos_hint = {"x": 0.01, "top": 1.4})
        self.labelEstimation = Label (text = "estimation", font_size = dp(20), color = (0.5, 0.5, 0.5, 1), pos_hint = {"x" : 0.01, "top": 1.25})
        self.labelLastTry = Label (text = "Last attempt: 0% for 0 throws", font_size = dp(19), color = (0.5, 0.5, 0.5, 1), pos_hint = {"x": 0.01, "top": 0.66})
        self.labelTheBestTry = Label(text = "The best attempt: 0% for 0 throws", font_size = dp(19), color = (0.5, 0.5, 0.5, 1), pos_hint = {"x": 0.01, "top": 0.62})

        Box.add_widget(buttonGot)
        Box.add_widget(buttonMissed)
        Box.add_widget(self.labelHits)
        Box.add_widget(self.labelBlunders)
        Box.add_widget(self.labelPercent)
        Box.add_widget(self.labelFullThrows)
        Box.add_widget(buttonReset)
        Box.add_widget(self.labelName)
        Box.add_widget(self.labelEstimation)
        Box.add_widget(self.labelLastTry)
        Box.add_widget(self.labelTheBestTry)
        Box.add_widget(logo)

        return Box

Application().run()