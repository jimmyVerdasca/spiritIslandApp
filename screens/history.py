from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


class HistoryScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20)
        )


        self.add_top_bar(
            layout,
            "History"
        )


        self.history = MDLabel(
            text="No completed games.",
            halign="left",
            valign="top"
        )


        layout.add_widget(
            self.history
        )


        self.add_widget(layout)