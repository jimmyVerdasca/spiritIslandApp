# ============================================================
# main.py
# ============================================================

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout


from .screens.home import HomeScreen
from .screens.currentGames import CurrentGamesScreen
from .screens.newGame import NewGameScreen
from .screens.trophies import TrophyScreen
from .screens.history import HistoryScreen
from .screens.finisfGame import FinishGameScreen
from .screens.settings import SettingsScreen

from .screens.widgets.app_background import AppBackground

from .managers.language_manager import LanguageManager
from .managers.theme_manager import ThemeManager
from .managers.settings_manager import SettingsManager
from .managers.music_manager import MusicManager
from .managers.assets_manager import AssetManager

from shared.data_access.factory import create_data_provider
from config.active import *


class SpiritIslandApp(MDApp):

    icon = AssetManager.path("home", "logoApp.png")

    def __init__(
        self,
        **kwargs,
    ):

        super().__init__(
            **kwargs
        )

        # ====================================================
        # Managers
        #
        # IMPORTANT:
        # SettingsManager must be created FIRST because
        # LanguageManager and ThemeManager load their initial
        # values from it.
        # ====================================================

        self.settings_manager = (
            SettingsManager()
        )

        self.language_manager = (
            LanguageManager(
                self.settings_manager.get(
                    "language"
                )
            )
        )

        self.theme_manager = (
            ThemeManager(
                theme=self.settings_manager.get(
                    "theme"
                ),
                theme_file=self.settings_manager.get(
                    "theme_file"
                ),
            )
        )


        self.data = create_data_provider(
            user_data_dir=self.user_data_dir,
        )

    # ========================================================
    # Build
    # ========================================================

    def build(self):

        # ====================================================
        # KivyMD global theme
        # ====================================================

        self.theme_cls.primary_palette = "Green"

        self._sync_kivymd_theme()

        # ====================================================
        # Root
        # ====================================================

        root = FloatLayout()

        background = AppBackground()

        root.add_widget(
            background
        )

        # ====================================================
        # Screen manager
        # ====================================================

        screen_manager = ScreenManager()

        screen_manager.add_widget(
            HomeScreen(
                name="home", data=self.data
            )
        )

        screen_manager.add_widget(
            CurrentGamesScreen(
                name="current", data=self.data
            )
        )

        screen_manager.add_widget(
            NewGameScreen(
                name="new", data=self.data
            )
        )

        screen_manager.add_widget(
            TrophyScreen(
                name="trophies", data=self.data
            )
        )

        screen_manager.add_widget(
            HistoryScreen(
                name="history", data=self.data
            )
        )

        screen_manager.add_widget(
            FinishGameScreen(
                name="finish", data=self.data
            )
        )

        screen_manager.add_widget(
            SettingsScreen(
                name="settings", data=self.data
            )
        )

        # ====================================================
        # Music
        # ====================================================

        try:

            MusicManager.start()

        except Exception as error:

            print(
                "MusicManager failed to start:",
                error,
            )

        # ====================================================
        # Add screens above background
        # ====================================================

        root.add_widget(
            screen_manager
        )

        return root

    # ========================================================
    # KivyMD theme synchronization
    # ========================================================

    def _sync_kivymd_theme(self):

        if (
            self.theme_manager.current_theme
            == "dark"
        ):

            self.theme_cls.theme_style = "Dark"

        else:

            self.theme_cls.theme_style = "Light"

    # ========================================================
    # Stop
    # ========================================================

    def on_stop(self):

        try:

            MusicManager.stop()

        except Exception:
            pass

        return super().on_stop()


if __name__ == "__main__":

    SpiritIslandApp().run()