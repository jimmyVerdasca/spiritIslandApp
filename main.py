from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.home import HomeScreen


class SpiritIslandApp(App):

    def build(self):

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen()
        )

        return manager


if __name__ == "__main__":
    SpiritIslandApp().run()