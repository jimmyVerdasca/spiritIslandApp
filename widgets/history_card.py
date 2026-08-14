from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

from engine.formatter import format_game
from engine.scoring import (
    calculate_game_difficulty,
    calculate_score_breakdown,
)


class HistoryCard(MDCard):

    """
    Card displaying a completed game's summary
    and score breakdown.

    Game data and scoring are handled by the engine.
    UI construction is handled here through the
    application's WidgetFactory.
    """

    def __init__(
        self,
        game,
        widget_factory,
        theme,
        language_manager,
        **kwargs,
    ):

        super().__init__(
            **kwargs
        )

        self.game = game
        self.widget_factory = widget_factory
        self.theme = theme
        self.language_manager = language_manager

        self.build()


    # ====================================================
    # Build
    # ====================================================

    def build(self):

        # ------------------------------------------------
        # Card configuration
        # ------------------------------------------------

        self.orientation = "vertical"

        self.adaptive_height = True

        self.padding = self.theme.dimension(
            "card",
            "padding",
        )

        self.spacing = self.theme.spacing(
            "sm"
        )

        self.radius = [
            self.theme.dimension(
                "card",
                "radius",
            )
        ]

        self.elevation = 3


        # ------------------------------------------------
        # Background
        # ------------------------------------------------

        background = self.theme.get(
            "card"
        )

        if background is not None:

            self.md_bg_color = background


        # ------------------------------------------------
        # Result border
        # ------------------------------------------------

        if self.game.result == "Victory":

            result_color = "button"

        else:

            result_color = "selection_warning"


        self.app_line_color = result_color

        line_color = self.theme.get(
            result_color
        )

        if line_color is not None:

            self.line_color = line_color


        self.line_width = self.theme.spacing(
            "xs"
        )


        # ------------------------------------------------
        # Columns
        # ------------------------------------------------

        columns = MDBoxLayout(

            orientation="horizontal",

            spacing=self.theme.spacing(
                "lg"
            ),

            adaptive_height=True,
        )


        columns.add_widget(
            self.build_game_summary()
        )

        columns.add_widget(
            self.build_score_summary()
        )


        self.add_widget(
            columns
        )


    # ====================================================
    # Game summary
    # ====================================================

    def build_game_summary(self):

        game_summary = MDBoxLayout(

            orientation="vertical",

            adaptive_height=True,

            spacing=self.theme.spacing(
                "xs"
            ),
        )


        # ------------------------------------------------
        # Game title
        # ------------------------------------------------

        game_label = self.widget_factory.create_label(

            text=(
                f"{self.language_manager.get('game')} "
                f"#{self.game.id}"
            ),

            style="subtitle",

            color="text_primary",

            size_hint_y=None,
        )


        game_label.bold = True

        self.bind_label_height(
            game_label
        )


        # ------------------------------------------------
        # Game details
        # ------------------------------------------------

        game_details = self.widget_factory.create_label(

            text=str(
                format_game(
                    self.game
                )
            ),

            style="secondary",

            color="card_text_secondary",

            size_hint_y=None,
        )


        self.bind_label_height(
            game_details
        )


        # ------------------------------------------------
        # Build
        # ------------------------------------------------

        game_summary.add_widget(
            game_label
        )

        game_summary.add_widget(
            game_details
        )


        return game_summary


    # ====================================================
    # Score summary
    # ====================================================

    def build_score_summary(self):

        score_summary = MDBoxLayout(

            orientation="vertical",

            adaptive_height=True,

            spacing=self.theme.spacing(
                "xs"
            ),
        )


        # ------------------------------------------------
        # Difficulty
        # ------------------------------------------------

        (
            adversary_difficulty,
            scenario_difficulty,
        ) = calculate_game_difficulty(
            self.game
        )


        # ------------------------------------------------
        # Score breakdown
        # ------------------------------------------------

        breakdown = calculate_score_breakdown(

            result=self.game.result,

            scenario_difficulty=scenario_difficulty,

            adversary_difficulty=adversary_difficulty,

            players=self.game.players,

            invader_cards=self.game.invader_cards_remaining,

            dahan=self.game.dahan_remaining,

            blight=self.game.blight_remaining,
        )


        # ------------------------------------------------
        # Translations
        # ------------------------------------------------

        result_text = (

            self.language_manager.get(
                "victory"
            )

            if self.game.result == "Victory"

            else

            self.language_manager.get(
                "defeat"
            )
        )


        difficulty_text = (
            self.language_manager.get(
                "difficulty"
            )
        )


        adversaries_label = (
            self.language_manager.get(
                "adversaries_title"
            )
        )


        scenario_text = (
            self.language_manager.get(
                "scenario"
            )
        )


        final_board_text = (
            self.language_manager.get(
                "final_board_state"
            )
        )


        invader_cards_text = (
            self.language_manager.get(
                "invader_cards"
            )
        )


        dahan_text = (
            self.language_manager.get(
                "dahan"
            )
        )


        blight_text = (
            self.language_manager.get(
                "blight"
            )
        )


        final_score_text = (
            self.language_manager.get(
                "final_score"
            )
        )


        # ------------------------------------------------
        # Score multipliers
        # ------------------------------------------------

        difficulty_multiplier = (

            5

            if self.game.result == "Victory"

            else 2
        )


        invader_multiplier = (

            2

            if self.game.result == "Victory"

            else 1
        )


        # ------------------------------------------------
        # Score display
        # ------------------------------------------------

        score_text = (

            f"{result_text}\n\n"

            f"{difficulty_text}\n"

            f"   {adversaries_label}: "
            f"{adversary_difficulty} × "
            f"{difficulty_multiplier}\n"

            f"   {scenario_text}: "
            f"{scenario_difficulty} × "
            f"{difficulty_multiplier}\n\n"

            f"{final_board_text}\n"

            f"   {invader_cards_text}: "
            f"{self.game.invader_cards_remaining} × "
            f"{invader_multiplier} "
            f"= +{breakdown['invader_bonus']}\n"

            f"   {dahan_text}: "
            f"{self.game.dahan_remaining} / "
            f"{self.game.players} "
            f"= +{breakdown['survival_bonus']}\n"

            f"   {blight_text}: "
            f"-{self.game.blight_remaining} / "
            f"{self.game.players} "
            f"= {breakdown['blight_bonus']}\n\n"

            f"{final_score_text}: "
            f"{self.game.score}"
        )


        # ------------------------------------------------
        # Score label
        # ------------------------------------------------

        score_label = self.widget_factory.create_label(

            text=score_text,

            style="secondary",

            color="card_text_secondary",

            size_hint_y=None,
        )


        self.bind_label_height(
            score_label
        )


        score_summary.add_widget(
            score_label
        )


        return score_summary


    # ====================================================
    # Helpers
    # ====================================================

    @staticmethod
    def bind_label_height(
        label,
    ):

        label.bind(

            texture_size=lambda instance, value:

            setattr(
                instance,
                "height",
                value[1],
            )
        )
