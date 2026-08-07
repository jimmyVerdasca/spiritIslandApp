from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

from database.database import get_trophies

from widgets.trophy_card import TrophyCard

from kivymd.uix.progressbar import MDProgressBar


class TrophyScreen(BaseScreen):
    
    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10)
        )


        self.add_top_bar(
            layout,
            "Trophies"
        )


        self.progress_label = MDLabel(
            text="Trophies: 0 / 0",
            adaptive_height=True,
            halign="center"
        )

        layout.add_widget(
            self.progress_label
        )


        self.progress = MDProgressBar(
            value=0,
            max=100,
            size_hint_y=None,
            height=dp(15)
        )


        layout.add_widget(
            self.progress
        )


        scroll = MDScrollView()


        self.container = MDGridLayout(
            cols=3,
            spacing=dp(15),
            padding=dp(10),
            adaptive_height=True
        )


        scroll.add_widget(
            self.container
        )


        layout.add_widget(
            scroll
        )


        self.add_widget(
            layout
        )


    def on_enter(self):

        self.refresh_trophies()



    def refresh_trophies(self):

        self.container.clear_widgets()


        trophies = get_trophies()


        total = len(trophies)

        unlocked = len(
            [
                t
                for t in trophies
                if t.unlocked
            ]
        )


        self.progress_label.text = (
            f"Trophies: {unlocked} / {total}"
        )


        if total:

            self.progress.value = (
                unlocked / total * 100
            )


        for trophy in trophies:

            self.container.add_widget(
                TrophyCard(trophy)
            )