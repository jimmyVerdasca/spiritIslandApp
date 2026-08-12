from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from database.database import (
    get_running_games,
    abandon_game as db_abandon_game,
)

from engine.formatter import format_game


class CurrentGamesScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # =================================================
        # Managers
        # =================================================

        app = MDApp.get_running_app()

        self.settings_manager = app.settings_manager
        self.language_manager = app.language_manager
        self.theme_manager = app.theme_manager


        # =================================================
        # Pagination
        # =================================================

        self.page_size = 20

        self.current_offset = 0

        self.loading = False

        self.finished_loading = False


        # =================================================
        # Main layout
        # =================================================

        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
        )


        # =================================================
        # Top bar
        # =================================================

        self.add_top_bar(
            self.layout,
            self.language_manager.get(
                "current_games"
            )
        )


        # =================================================
        # Scroll view
        # =================================================

        self.scroll = MDScrollView()


        self.games_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(15),
            adaptive_height=True,
        )


        self.scroll.add_widget(
            self.games_layout
        )


        self.layout.add_widget(
            self.scroll
        )


        self.add_widget(
            self.layout
        )


        # =================================================
        # Infinite scrolling
        # =================================================

        self.scroll.bind(
            scroll_y=self.check_scroll
        )


        # =================================================
        # Apply theme
        # =================================================

        self.update_theme()


    # ====================================================
    # Screen lifecycle
    # ====================================================

    def on_enter(self):

        self.update_top_bar()

        self.update_theme()

        self.refresh_games()


    # ====================================================
    # Top bar
    # ====================================================

    def update_top_bar(self):

        # BaseScreen should expose the title label.
        # See the BaseScreen change below.

        if hasattr(
            self,
            "top_bar_title"
        ):

            self.top_bar_title.text = (
                self.language_manager.get(
                    "current_games"
                )
            )


    # ====================================================
    # Theme
    # ====================================================

    def update_theme(self):

        # Main screen background

        self.layout.md_bg_color = (
            self.theme_manager.get(
                "background"
            )
        )


    # ====================================================
    # Scroll
    # ====================================================

    def check_scroll(
        self,
        instance,
        value,
    ):

        if self.finished_loading:
            return


        if value < 0.1:

            self.load_more_games()


    # ====================================================
    # Refresh games
    # ====================================================

    def refresh_games(self):

        self.current_offset = 0

        self.finished_loading = False

        self.games_layout.clear_widgets()

        self.load_more_games()


    # ====================================================
    # Load more games
    # ====================================================

    def load_more_games(self):

        if self.loading:
            return


        if self.finished_loading:
            return


        self.loading = True


        games = get_running_games(
            limit=self.page_size,
            offset=self.current_offset,
        )


        # ---------------------------------------------
        # No more games
        # ---------------------------------------------

        if not games:

            if self.current_offset == 0:

                empty_label = MDLabel(
                    text=self.language_manager.get(
                        "no_running_games"
                    ),
                    halign="center",
                    size_hint_y=None,
                    height=dp(50),
                )


                empty_label.theme_text_color = "Custom"

                empty_label.text_color = (
                    self.theme_manager.get(
                        "text_secondary"
                    )
                )


                self.games_layout.add_widget(
                    empty_label
                )


            self.finished_loading = True

            self.loading = False

            return


        # ---------------------------------------------
        # Add games
        # ---------------------------------------------

        for game in games:

            self.add_game_card(
                game
            )


        self.current_offset += len(
            games
        )


        # If fewer results than page size,
        # we reached the end.

        if len(games) < self.page_size:

            self.finished_loading = True


        self.loading = False


    # ====================================================
    # Game card
    # ====================================================

    def add_game_card(
        self,
        game,
    ):

        # ---------------------------------------------
        # Card
        # ---------------------------------------------

        card = MDCard(
            orientation="vertical",
            padding=[
                dp(20),
                dp(15),
            ],
            spacing=dp(10),
            size_hint_y=None,
            adaptive_height=True,
            radius=[20],
        )


        card.md_bg_color = (
            self.theme_manager.get(
                "card"
            )
        )


        # ---------------------------------------------
        # Header row
        # ---------------------------------------------

        header_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
        )


        # ---------------------------------------------
        # Header
        # ---------------------------------------------

        header = MDLabel(
            text=(
                f"{self.language_manager.get('game')} "
                f"#{game.id}"
            ),
            font_style="H6",
            valign="center",
            size_hint_x=1,
        )


        header.theme_text_color = "Custom"

        header.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )


        # ---------------------------------------------
        # Finish button
        # ---------------------------------------------

        finish_button = MDIconButton(
            icon="flag-checkered",
            size_hint_x=None,
            width=dp(40),
        )


        finish_button.theme_icon_color = "Custom"

        finish_button.icon_color = (
            self.theme_manager.get(
                "icon"
            )
        )


        finish_button.bind(
            on_release=lambda x, g=game:
            self.open_finish_game(
                g
            )
        )


        # ---------------------------------------------
        # Abandon button
        # ---------------------------------------------

        abandon_button = MDIconButton(
            icon="close-circle-outline",
            size_hint_x=None,
            width=dp(40),
        )


        abandon_button.theme_icon_color = "Custom"

        # Optional dedicated destructive color.
        # Falls back to the normal icon color for now.

        abandon_button.icon_color = (
            self.theme_manager.get(
                "icon"
            )
        )


        abandon_button.bind(
            on_release=lambda x, game_id=game.id:
            self.confirm_abandon(
                game_id
            )
        )


        header_row.add_widget(
            header
        )

        header_row.add_widget(
            finish_button
        )

        header_row.add_widget(
            abandon_button
        )


        # ---------------------------------------------
        # Game details
        # ---------------------------------------------

        details = MDLabel(
            text=format_game(game),
            size_hint_y=None,
            adaptive_height=True,
            halign="left",
            valign="top",
        )


        details.theme_text_color = "Custom"

        details.text_color = (
            self.theme_manager.get(
                "card_text_secondary"
            )
        )


        details.bind(
            texture_size=details.setter(
                "size"
            )
        )


        # ---------------------------------------------
        # Add to card
        # ---------------------------------------------

        card.add_widget(
            header_row
        )

        card.add_widget(
            details
        )


        self.games_layout.add_widget(
            card
        )


    # ====================================================
    # Abandon game
    # ====================================================

    def abandon_game(
        self,
        game_id,
    ):

        self.dialog.dismiss()

        db_abandon_game(
            game_id
        )

        self.refresh_games()


    # ====================================================
    # Confirm abandon
    # ====================================================

    def confirm_abandon(
        self,
        game_id,
    ):

        self.dialog = MDDialog(

            title=self.language_manager.get(
                "abandon_game_title"
            ),

            text=self.language_manager.get(
                "abandon_game_message"
            ),

            buttons=[

                MDFlatButton(
                    text=self.language_manager.get(
                        "cancel"
                    ),
                    on_release=lambda x:
                    self.dialog.dismiss(),
                ),

                MDFlatButton(
                    text=self.language_manager.get(
                        "abandon"
                    ),
                    on_release=lambda x:
                    self.abandon_game(
                        game_id
                    ),
                ),

            ],
        )


        self.dialog.open()


    # ====================================================
    # Finish game
    # ====================================================

    def open_finish_game(
        self,
        game,
    ):

        self.navigate_to(
            "finish",
            previous="current",
            game=game,
        )