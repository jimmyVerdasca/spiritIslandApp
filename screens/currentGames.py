from .baseScreen import BaseScreen

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton

from database.database import get_running_games, abandon_game as db_abandon_game
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
            padding=["20dp", "15dp"],
            spacing="10dp",
            size_hint_y=None,
            adaptive_height=True,
            radius=[20]
        )

        # Header row
        header_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="40dp",
        )

        header = MDLabel(
            text=f"Game #{game.id}",
            font_style="H6",
            valign="center",
            size_hint_x=1
        )

        abandon_button = MDIconButton(
            icon="close-circle-outline",
            size_hint_x=None,
            width="40dp"
        )

        abandon_button.bind(
            on_release=lambda x, game_id=game.id:
                self.confirm_abandon(game_id)
        )

        finish_button = MDIconButton(
            icon="flag-checkered",
            size_hint_x=None,
            width="40dp"
        )

        finish_button.bind(
            on_release=lambda x, g=game:
                self.open_finish_game(g)
        )

        header_row.add_widget(header)
        header_row.add_widget(finish_button)
        header_row.add_widget(abandon_button)


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


        card.add_widget(header_row)
        card.add_widget(details)

        self.games_layout.add_widget(card)

    def abandon_game(self, game_id):
    
        self.dialog.dismiss()

        db_abandon_game(game_id)

        self.refresh_games()

    def confirm_abandon(self, game_id):
    
        self.dialog = MDDialog(
            title="Abandon game?",
            text=(
                "This will remove this game from your running games.\n"
                "You will not be able to see it anymore."
            ),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x:
                        self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="ABANDON",
                    on_release=lambda x:
                        self.abandon_game(game_id)
                ),
            ],
        )

        self.dialog.open()

    def open_finish_game(self, game):
    
        self.navigate_to(
            "finish",
            previous="current",
            game=game
        )