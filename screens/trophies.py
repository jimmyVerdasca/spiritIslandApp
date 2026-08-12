from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar

from database.database import get_trophies

from widgets.trophy_card import TrophyCard


class TrophyScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # --------------------------------------------
        # Main layout
        # --------------------------------------------

        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10),
        )


        # --------------------------------------------
        # Top bar
        # --------------------------------------------

        self.add_top_bar(
            layout,
            "trophies",
        )


        # --------------------------------------------
        # Progress label
        # --------------------------------------------

        self.progress_label = MDLabel(
            adaptive_height=True,
            halign="center",
        )


        layout.add_widget(
            self.progress_label
        )


        # --------------------------------------------
        # Progress bar
        # --------------------------------------------

        self.progress = MDProgressBar(
            value=0,
            max=100,
            size_hint_y=None,
            height=dp(15),
        )


        layout.add_widget(
            self.progress
        )


        # --------------------------------------------
        # Scroll
        # --------------------------------------------

        scroll = MDScrollView()


        self.container = MDGridLayout(
            cols=3,
            spacing=dp(15),
            padding=dp(10),
            adaptive_height=True,
        )


        scroll.add_widget(
            self.container
        )


        layout.add_widget(
            scroll
        )


        # --------------------------------------------
        # Add screen
        # --------------------------------------------

        self.add_widget(
            layout
        )


        # --------------------------------------------
        # Initial UI
        # --------------------------------------------

        self.refresh_ui()


    # ====================================================
    # Lifecycle
    # ====================================================

    def on_pre_enter(self):

        # Important:
        # This updates the BaseScreen top bar
        # translation and theme.

        super().on_pre_enter()

        self.refresh_ui()


    # ====================================================
    # UI refresh
    # ====================================================

    def refresh_ui(self):

        self.update_text()

        self.update_theme()

        self.refresh_trophies()


    # ====================================================
    # Translation
    # ====================================================

    def update_text(self):

        self.progress_label.text = (
            self.language_manager.get(
                "trophies_progress"
            ).format(
                unlocked=0,
                total=0,
            )
        )


    # ====================================================
    # Theme
    # ====================================================

    def update_theme(self):

        # --------------------------------------------
        # Progress label
        # --------------------------------------------

        self.progress_label.theme_text_color = (
            "Custom"
        )

        self.progress_label.text_color = (
            self.theme_manager.get(
                "text_secondary"
            )
        )


        # --------------------------------------------
        # Progress bar
        # --------------------------------------------

        self.progress.color = (
            self.theme_manager.get(
                "progress"
            )
        )


    # ====================================================
    # Trophies
    # ====================================================

    def refresh_trophies(self):

        self.container.clear_widgets()


        trophies = get_trophies()


        total = len(
            trophies
        )


        unlocked = len(
            [
                trophy
                for trophy in trophies
                if trophy.unlocked
            ]
        )


        # --------------------------------------------
        # Progress label
        # --------------------------------------------

        self.progress_label.text = (
            self.language_manager.get(
                "trophies_progress"
            ).format(
                unlocked=unlocked,
                total=total,
            )
        )


        # --------------------------------------------
        # Progress
        # --------------------------------------------

        if total:

            self.progress.value = (
                unlocked / total * 100
            )

        else:

            self.progress.value = 0


        # --------------------------------------------
        # Trophy cards
        # --------------------------------------------

        for trophy in trophies:

            self.container.add_widget(
                TrophyCard(
                    trophy
                )
            )