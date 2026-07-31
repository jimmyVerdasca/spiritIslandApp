from .baseScreen import BaseScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout


class CurrentGamesScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            padding="20dp"
        )


        self.add_top_bar(
            layout,
            "Current Games"
        )


        title = MDLabel(
            text="Current Games",
            halign="center",
            font_style="H4"
        )

        layout.add_widget(title)


        # your screen content here




        self.add_widget(layout)