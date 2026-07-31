from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


class TrophyScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20)
        )


        self.add_top_bar(
            layout,
            "Trophies"
        )


        title = MDLabel(
            text="Trophies",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(60)
        )


        self.trophies = MDLabel(
            text="No trophies unlocked yet.",
            halign="left",
            valign="top"
        )


        layout.add_widget(title)

        layout.add_widget(
            self.trophies
        )


        self.add_widget(layout)