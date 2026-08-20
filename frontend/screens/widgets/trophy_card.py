from kivymd.app import MDApp

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from kivy.uix.image import Image
from kivy.metrics import dp


class TrophyCard(MDCard):

    TROPHY_IMAGE_PATH = "assets/trophies/"

    def __init__(self, trophy, **kwargs):

        super().__init__(**kwargs)

        # --------------------------------------------
        # Managers
        # --------------------------------------------

        app = MDApp.get_running_app()

        self.language_manager = app.language_manager
        self.theme_manager = app.theme_manager

        # --------------------------------------------
        # State
        # --------------------------------------------

        self.trophy = trophy

        # --------------------------------------------
        # Card
        # --------------------------------------------

        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(5)

        self.size_hint_y = None
        self.height = dp(200)

        # --------------------------------------------
        # Image
        # --------------------------------------------

        self.image = Image(
            source=(
                self.TROPHY_IMAGE_PATH
                + (
                    trophy.unlocked_image
                    if trophy.unlocked
                    else trophy.locked_image
                )
            ),
            allow_stretch=True,
            keep_ratio=True,
        )

        self.add_widget(
            self.image
        )

        # --------------------------------------------
        # Name
        # --------------------------------------------

        self.name_label = MDLabel(
            halign="center",
            bold=True,
            adaptive_height=True,
        )

        self.add_widget(
            self.name_label
        )

        # --------------------------------------------
        # Description
        # --------------------------------------------

        self.description_label = MDLabel(
            halign="center",
            adaptive_height=True,
        )

        self.add_widget(
            self.description_label
        )

        # --------------------------------------------
        # Initial text
        # --------------------------------------------

        self.update_text()

        # --------------------------------------------
        # Theme
        # --------------------------------------------

        self.update_theme()

    # ====================================================
    # Translation
    # ====================================================

    def update_text(self):

        # Get the complete trophies translation section
        trophies = self.language_manager.get(
            "trophies"
        )

        # Safety check
        if not isinstance(trophies, dict):
            self.name_label.text = self.trophy.key
            self.description_label.text = self.trophy.key
            return

        # Get this specific trophy
        trophy_translation = trophies.get(
            self.trophy.key
        )

        # Safety check
        if not isinstance(trophy_translation, dict):
            self.name_label.text = self.trophy.key
            self.description_label.text = self.trophy.key
            return

        # --------------------------------------------
        # Name
        # --------------------------------------------

        self.name_label.text = (
            trophy_translation.get(
                "name",
                self.trophy.key,
            )
        )

        # --------------------------------------------
        # Description
        # --------------------------------------------

        self.description_label.text = (
            trophy_translation.get(
                "description",
                self.trophy.key,
            )
        )

    # ====================================================
    # Theme
    # ====================================================

    def update_theme(self):

        # --------------------------------------------
        # Card background
        # --------------------------------------------

        if self.trophy.unlocked:

            self.md_bg_color = (
                self.theme_manager.get(
                    "trophy_unlocked"
                )
            )

        else:

            self.md_bg_color = (
                self.theme_manager.get(
                    "trophy_locked"
                )
            )

        # --------------------------------------------
        # Name
        # --------------------------------------------

        self.name_label.theme_text_color = (
            "Custom"
        )

        self.name_label.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )

        # --------------------------------------------
        # Description
        # --------------------------------------------

        self.description_label.theme_text_color = (
            "Custom"
        )

        self.description_label.text_color = (
            self.theme_manager.get(
                "text_secondary"
            )
        )

    # ====================================================
    # Refresh
    # ====================================================

    def refresh_ui(self):

        self.update_text()
        self.update_theme()
