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
        self.page_size = 20
        self.current_offset = 0
        self.loading = False
        self.finished_loading = False


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

        scroll.bind(
            scroll_y=self.check_scroll
        )

    def check_scroll(self, instance, value):

        if self.finished_loading:
            return
        
        if value < 0.1:
            self.load_more_games()

    def on_enter(self):

        self.refresh_games()



    def refresh_games(self):
    
        self.current_offset = 0

        self.games_layout.clear_widgets()

        self.load_more_games()

    def load_more_games(self):
    
        if self.loading:
            return

        self.loading = True

        games = get_running_games(
            limit=self.page_size,
            offset=self.current_offset
        )

        if not games:

            if self.current_offset == 0:
                self.games_layout.add_widget(
                    MDLabel(
                        text="No running games",
                        halign="center",
                        size_hint_y=None,
                        height="50dp"
                    )
                )

            self.loading = False
            return


        for game in games:
            self.add_game_card(game)


        self.current_offset += len(games)

        self.loading = False

    def add_game_card(self, game):
        
        card = MDCard(
            orientation="vertical",
            padding=["20dp","15dp"],
            spacing="10dp",
            size_hint_y=None,
            adaptive_height=True,
            radius=[20]
        )

        header = MDLabel(
            text=f"Game #{game.id}",
            font_style="H6",
            size_hint_y=None,
            height="35dp"
        )

        details = MDLabel(
            text=format_game(game),
            size_hint_y=None,
            adaptive_height=True,
            halign="left",
            valign="top"
        )

        details.bind(
            texture_size=details.setter("size")
        )

        card.add_widget(header)
        card.add_widget(details)

        self.games_layout.add_widget(card)