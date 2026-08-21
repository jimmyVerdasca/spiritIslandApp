from kivymd.uix.boxlayout import MDBoxLayout

from shared.engine.formatter import format_game


class CurrentGameCard:

    """
    Builds the visual representation of a running game.

    The card is responsible only for presentation.

    Database operations, dialogs, and navigation remain
    in CurrentGamesScreen.
    """

    def __init__(
        self,
        screen,
        game,
        on_finish,
        on_abandon,
    ):

        self.screen = screen
        self.game = game

        self.on_finish = on_finish
        self.on_abandon = on_abandon


    # ====================================================
    # Builds
    # =============s=======================================

    def build(self):

        card = self.screen.create_card(

            orientation="vertical",

            adaptive_height=True,

            padding=self.screen.dimension(
                "card",
                "padding",
            ),

            spacing=self.screen.spacing(
                "sm"
            ),
        )


        # ====================================================
        # Header
        # ====================================================

        header_row = MDBoxLayout(

            orientation="horizontal",

            size_hint_y=None,

            height=self.screen.dimension(
                "button",
                "height",
            ),

            spacing=self.screen.spacing(
                "xs"
            ),
        )


        # ------------------------------------------------
        # Title
        # ------------------------------------------------

        header = self.screen.create_label(

            text=(
                f"{self.screen.language_manager.get('game')} "
                f"#{self.game.id}"
            ),

            style="subtitle",

            color="text_primary",

            halign="left",

            valign="center",

            size_hint_x=1,

            size_hint_y=None,
        )


        header.bold = True


        header.bind(

            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )


        # ------------------------------------------------
        # Finish button
        # ------------------------------------------------

        finish_button = (
            self.screen.create_icon_button(

                icon="flag-checkered",

                size="medium",

                background_color="card",

                icon_color="icon",
            )
        )


        finish_button.bind(

            on_release=lambda instance:
            self.on_finish(
                self.game
            )
        )


        # ------------------------------------------------
        # Abandon button
        # ------------------------------------------------

        abandon_button = (
            self.screen.create_icon_button(

                icon="close-circle-outline",

                size="medium",

                background_color="card",

                icon_color="icon",
            )
        )


        abandon_button.bind(

            on_release=lambda instance:
            self.on_abandon(
                self.game.id
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


        # ====================================================
        # Details
        # ====================================================

        details = self.screen.create_label(

            text=str(
                format_game(
                    self.game
                )
            ),

            style="secondary",

            color="card_text_secondary",

            halign="left",

            valign="top",

            size_hint_y=None,
        )


        details.bind(

            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )


        # ====================================================
        # Build
        # ====================================================

        card.add_widget(
            header_row
        )

        card.add_widget(
            details
        )


        return card