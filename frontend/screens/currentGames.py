from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from shared.engine.formatter import format_game

from .widgets.current_game_card import CurrentGameCard
from .baseScreen import BaseScreen

class CurrentGamesScreen(BaseScreen):

    """
    Display currently running games.

    Responsibilities:

        - Pagination.
        - Loading running games.
        - Abandon confirmation.
        - Navigation to finish screen.

    Card construction is handled by CurrentGameCard.
    """


    def __init__(
        self,
        **kwargs,
    ):

        super().__init__(
            **kwargs
        )


        # ====================================================
        # Pagination
        # ====================================================

        self.page_size = 20

        self.current_offset = 0

        self.loading = False

        self.finished_loading = False

        self.dialog = None


        # ====================================================
        # Main layout
        # ====================================================

        self.layout = MDBoxLayout(

            orientation="vertical",

            spacing=self.spacing(
                "sm"
            ),

            padding=self.dimension(
                "screen",
                "padding",
            ),
        )


        self.add_top_bar(
            self.layout,
            "current_games",
        )


        # ====================================================
        # Scroll
        # ====================================================

        self.scroll = MDScrollView()


        self.games_layout = MDBoxLayout(

            orientation="vertical",

            spacing=self.spacing(
                "sm"
            ),

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


        # ====================================================
        # Infinite scrolling
        # ====================================================

        self.scroll.bind(
            scroll_y=self.check_scroll
        )


    # ====================================================
    # Lifecycle
    # ====================================================

    def on_pre_enter(
        self,
    ):

        super().on_pre_enter()

        self.refresh_games()


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

        if self.loading:
            return

        if value < 0.1:

            self.load_more_games()


    # ====================================================
    # Refresh
    # ====================================================

    def refresh_games(
        self,
    ):

        self.current_offset = 0

        self.loading = False

        self.finished_loading = False

        self.games_layout.clear_widgets()

        self.load_more_games()


    # ====================================================
    # Load games
    # ====================================================

    def load_more_games(
        self,
    ):

        if self.loading:
            return

        if self.finished_loading:
            return


        self.loading = True


        games = self.data.get_running_games(

            limit=self.page_size,

            offset=self.current_offset,
        )


        # ------------------------------------------------
        # No games
        # ------------------------------------------------

        if not games:

            if self.current_offset == 0:

                self.show_empty_state()


            self.finished_loading = True

            self.loading = False

            return


        # ------------------------------------------------
        # Add cards
        # ------------------------------------------------

        for game in games:

            self.add_game_card(
                game
            )


        self.current_offset += len(
            games
        )


        if len(games) < self.page_size:

            self.finished_loading = True


        self.loading = False


    # ====================================================
    # Empty state
    # ====================================================

    def show_empty_state(
        self,
    ):

        label = self.create_label(

            text=str(
                self.language_manager.get(
                    "no_running_games"
                )
            ),

            style="body",

            color="text_secondary",

            halign="center",

            size_hint_y=None,
        )


        label.bind(

            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )


        self.games_layout.add_widget(
            label
        )


    # ====================================================
    # Game card
    # ====================================================

    def add_game_card(
        self,
        game,
    ):

        card_builder = CurrentGameCard(

            screen=self,

            game=game,

            on_finish=self.open_finish_game,

            on_abandon=self.confirm_abandon,
        )


        self.games_layout.add_widget(
            card_builder.build()
        )


    # ====================================================
    # Abandon
    # ====================================================

    def confirm_abandon(
        self,
        game_id,
    ):

        self.dialog = MDDialog(

            title=str(
                self.language_manager.get(
                    "abandon_game_title"
                )
            ),

            text=str(
                self.language_manager.get(
                    "abandon_game_message"
                )
            ),

            buttons=[

                MDFlatButton(

                    text=str(
                        self.language_manager.get(
                            "cancel"
                        )
                    ),

                    on_release=lambda instance:
                    self.dialog.dismiss(),
                ),

                MDFlatButton(

                    text=str(
                        self.language_manager.get(
                            "abandon"
                        )
                    ),

                    on_release=lambda instance:
                    self.abandon_game(
                        game_id
                    ),
                ),
            ],
        )


        self.dialog.open()


    def abandon_game(
        self,
        game_id,
    ):

        if self.dialog is not None:

            self.dialog.dismiss()

            self.dialog = None


        self.data.abandon_game(
            game_id
        )


        self.refresh_games()


    # ====================================================
    # Finish
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