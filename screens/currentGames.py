from .baseScreen import BaseScreen

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView

from database.database import get_running_games
from engine.formatter import format_game


class CurrentGamesScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        layout = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            spacing="10dp"
        )


        self.add_top_bar(
            layout,
            "Current Games"
        )


        scroll = MDScrollView()


        self.games_layout = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            padding="15dp",
            adaptive_height=True
        )


        scroll.add_widget(
            self.games_layout
        )


        layout.add_widget(scroll)


        self.add_widget(layout)



    def on_enter(self):

        self.refresh_games()



    def refresh_games(self):

        self.games_layout.clear_widgets()


        games = get_running_games()


        if not games:

            self.games_layout.add_widget(
                MDLabel(
                    text="No running games",
                    halign="center",
                    size_hint_y=None,
                    height="50dp"
                )
            )

            return



        for game in games:


            card = MDCard(
                orientation="vertical",

                padding=[
                    "20dp",
                    "15dp",
                    "20dp",
                    "15dp"
                ],

                size_hint_y=None,

                adaptive_height=True,

                radius=[
                    20,
                    20,
                    20,
                    20
                ],

                elevation=4
            )


            header = MDLabel(
                text=f"Game #{game.id}",
                font_style="H6",
                size_hint_y=None,
                height="35dp"
            )


            details = MDLabel(
                text=format_game(game),
                halign="left",
                valign="top",
                size_hint_y=None,
                adaptive_height=True
            )


            card.add_widget(header)
            card.add_widget(details)


            self.games_layout.add_widget(card)