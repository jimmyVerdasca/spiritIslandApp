from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from screens.home import HomeScreen
from screens.currentGames import CurrentGamesScreen
from screens.newGame import NewGameScreen
from screens.trophies import TrophyScreen
from screens.history import HistoryScreen


class SpiritIslandApp(MDApp):
    
    def build(self):

        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(name="home")
        )

        manager.add_widget(
            CurrentGamesScreen(name="current")
        )

        manager.add_widget(
            NewGameScreen(name="new")
        )

        manager.add_widget(
            TrophyScreen(name="trophies")
        )

        manager.add_widget(
            HistoryScreen(name="history")
        )

        return manager
    
if __name__ == "__main__":
    SpiritIslandApp().run()