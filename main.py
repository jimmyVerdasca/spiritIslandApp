from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from engine.music_manager import MusicManager

from screens.home import HomeScreen
from screens.currentGames import CurrentGamesScreen
from screens.newGame import NewGameScreen
from screens.trophies import TrophyScreen
from screens.history import HistoryScreen
from screens.finisfGame import FinishGameScreen
from widgets.app_background import AppBackground



class SpiritIslandApp(MDApp):
    icon = "assets/home/logoApp.png"
    
    def build(self):

        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"


        root = FloatLayout()
        background = AppBackground()
        root.add_widget(background)

        screen_manager = ScreenManager()

        screen_manager.add_widget(
            HomeScreen(name="home")
        )

        screen_manager.add_widget(
            CurrentGamesScreen(name="current")
        )

        screen_manager.add_widget(
            NewGameScreen(name="new")
        )

        screen_manager.add_widget(
            TrophyScreen(name="trophies")
        )

        screen_manager.add_widget(
            HistoryScreen(name="history")
        )

        screen_manager.add_widget(
            FinishGameScreen(name="finish")
        )

        MusicManager.start();
        root.add_widget(screen_manager)
        return root
    
if __name__ == "__main__":
    SpiritIslandApp().run()