from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDRaisedButton

from database.database import (
    get_finished_games,
    get_adversary_difficulty,
)

from engine.formatter import format_game
from engine.scoring import calculate_score_breakdown


class HistoryScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # --------------------------------------------
        # State
        # --------------------------------------------

        self.current_filter = "ALL"


        # --------------------------------------------
        # Main layout
        # --------------------------------------------

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20),
        )

        self.add_top_bar(
            layout,
            "history",
        )


        # --------------------------------------------
        # Filters
        # --------------------------------------------

        filter_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50),
        )

        self.all_button = MDRaisedButton(
            on_release=lambda x:
            self.set_filter("ALL"),
        )

        self.victory_button = MDRaisedButton(
            on_release=lambda x:
            self.set_filter("Victory"),
        )

        self.defeat_button = MDRaisedButton(
            on_release=lambda x:
            self.set_filter("Defeat"),
        )

        filter_box.add_widget(
            self.all_button
        )

        filter_box.add_widget(
            self.victory_button
        )

        filter_box.add_widget(
            self.defeat_button
        )

        layout.add_widget(
            filter_box
        )


        # --------------------------------------------
        # Scroll area
        # --------------------------------------------

        scroll = MDScrollView()

        self.container = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(10),
        )

        scroll.add_widget(
            self.container
        )

        layout.add_widget(
            scroll
        )


        # --------------------------------------------
        # Add screen
        # --------------------------------------------

        self.add_widget(
            layout
        )


        # --------------------------------------------
        # Initial UI
        # --------------------------------------------

        self.refresh_ui()


    # ====================================================
    # Lifecycle
    # ====================================================

    def on_pre_enter(self):

        super().on_pre_enter()

        self.refresh_ui()


    # ====================================================
    # UI refresh
    # ====================================================

    def refresh_ui(self):

        self.update_text()
        self.update_theme()
        self.refresh_history()


    # ====================================================
    # Translation
    # ====================================================

    def update_text(self):

        self.all_button.text = (
            self.language_manager.get(
                "all"
            )
        )

        self.victory_button.text = (
            self.language_manager.get(
                "victory"
            )
        )

        self.defeat_button.text = (
            self.language_manager.get(
                "defeat"
            )
        )


    # ====================================================
    # Theme
    # ====================================================

    def update_theme(self):

        self.update_filter_colors()


    # ====================================================
    # Filters
    # ====================================================

    def set_filter(self, filter_value):

        if filter_value not in (
            "ALL",
            "Victory",
            "Defeat",
        ):
            return

        self.current_filter = filter_value

        self.update_filter_colors()
        self.refresh_history()


    def update_filter_colors(self):

        inactive = (
            self.theme_manager.get(
                "inactive_button"
            )
        )

        active = (
            self.theme_manager.get(
                "button"
            )
        )

        if inactive is None:

            inactive = (
                0.5,
                0.5,
                0.5,
                1,
            )

        if active is None:

            active = (
                0.2,
                0.6,
                0.2,
                1,
            )

        self.all_button.md_bg_color = inactive
        self.victory_button.md_bg_color = inactive
        self.defeat_button.md_bg_color = inactive

        if self.current_filter == "ALL":

            self.all_button.md_bg_color = active

        elif self.current_filter == "Victory":

            self.victory_button.md_bg_color = active

        elif self.current_filter == "Defeat":

            self.defeat_button.md_bg_color = active


    # ====================================================
    # History loading
    # ====================================================

    def refresh_history(self):

        self.container.clear_widgets()

        if self.current_filter == "ALL":

            games = get_finished_games()

        else:

            games = get_finished_games(
                result=self.current_filter
            )

        if not games:

            label = MDLabel(
                text=self.language_manager.get(
                    "no_completed_games"
                ),
                adaptive_height=True,
                halign="center",
            )

            self.apply_label_theme(
                label,
                "text_secondary",
            )

            self.container.add_widget(
                label
            )

            return

        for game in games:

            self.container.add_widget(
                self.build_game_card(game)
            )


    # ====================================================
    # Game card
    # ====================================================

    def build_game_card(self, game):

        card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            adaptive_height=True,
            radius=[dp(20)],
        )

        # --------------------------------------------
        # Card background
        # --------------------------------------------

        card.md_bg_color = (
            self.theme_manager.get(
                "card"
            )
        )

        # --------------------------------------------
        # Result border
        # --------------------------------------------

        if game.result == "Victory":

            card.line_color = (
                self.theme_manager.get(
                    "button"
                )
            )

        else:

            card.line_color = (
                self.theme_manager.get(
                    "selection_warning"
                )
            )

        card.line_width = dp(2)


        # --------------------------------------------
        # Columns
        # --------------------------------------------

        columns = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            adaptive_height=True,
        )


        # --------------------------------------------
        # Left side
        # --------------------------------------------

        game_summary = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(5),
        )

        game_label = MDLabel(
            text=(
                f"{self.language_manager.get('game')} "
                f"#{game.id}"
            ),
            bold=True,
            adaptive_height=True,
        )

        self.apply_label_theme(
            game_label,
            "text_primary",
        )


        # --------------------------------------------
        # Translated adversary names
        # --------------------------------------------

        adversary_names = []

        for game_adversary in game.adversaries:

            adversary = game_adversary.adversary

            adversary_names.append(
                self.language_manager.get(
                    adversary.key,
                    "adversaries",
                )
            )

        adversaries_list = ", ".join(
            adversary_names
        )


        # --------------------------------------------
        # Left-side game details
        # --------------------------------------------

        game_details_text = (
            f"{format_game(game)}"
        )

        game_details = MDLabel(
            text=game_details_text,
            adaptive_height=True,
        )

        self.apply_label_theme(
            game_details,
            "card_text_secondary",
        )

        game_summary.add_widget(
            game_label
        )

        game_summary.add_widget(
            game_details
        )


        # --------------------------------------------
        # Right side
        # --------------------------------------------

        score_summary = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(5),
        )


        # --------------------------------------------
        # Calculate adversary difficulty
        # --------------------------------------------

        adversary_difficulty = 0

        for game_adversary in game.adversaries:

            if game_adversary.difficulty is None:
                continue

            difficulty = get_adversary_difficulty(
                game_adversary.adversary.id,
                game_adversary.difficulty.id,
            )

            if difficulty:

                adversary_difficulty += (
                    difficulty.score_difficulty
                )


        # --------------------------------------------
        # Calculate scenario difficulty
        # --------------------------------------------

        scenario_difficulty = sum(
            scenario.score_difficulty
            for scenario in game.scenarios
        )


        # --------------------------------------------
        # Score breakdown
        # --------------------------------------------

        breakdown = calculate_score_breakdown(
            result=game.result,
            scenario_difficulty=scenario_difficulty,
            adversary_difficulty=adversary_difficulty,
            players=game.players,
            invader_cards=game.invader_cards_remaining,
            dahan=game.dahan_remaining,
            blight=game.blight_remaining,
        )


        # --------------------------------------------
        # Translations
        # --------------------------------------------

        result_text = (
            self.language_manager.get(
                "victory"
            )
            if game.result == "Victory"
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


        # --------------------------------------------
        # Score display
        # --------------------------------------------

        difficulty_multiplier = (
            5
            if game.result == "Victory"
            else 2
        )

        invader_multiplier = (
            2
            if game.result == "Victory"
            else 1
        )

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
            f"{game.invader_cards_remaining} × "
            f"{invader_multiplier} "
            f"= +{breakdown['invader_bonus']}\n"

            f"   {dahan_text}: "
            f"{game.dahan_remaining} / "
            f"{game.players} "
            f"= +{breakdown['survival_bonus']}\n"

            f"   {blight_text}: "
            f"-{game.blight_remaining} / "
            f"{game.players} "
            f"= {breakdown['blight_bonus']}\n\n"

            f"{final_score_text}: "
            f"{game.score}"
        )


        score_label = MDLabel(
            text=score_text,
            adaptive_height=True,
        )

        self.apply_label_theme(
            score_label,
            "card_text_secondary",
        )

        score_summary.add_widget(
            score_label
        )


        # --------------------------------------------
        # Add columns
        # --------------------------------------------

        columns.add_widget(
            game_summary
        )

        columns.add_widget(
            score_summary
        )

        card.add_widget(
            columns
        )

        return card


    # ====================================================
    # Label theme helper
    # ====================================================

    def apply_label_theme(
        self,
        label,
        theme_key,
    ):

        label.theme_text_color = "Custom"

        color = (
            self.theme_manager.get(
                theme_key
            )
        )

        if color is not None:

            label.text_color = color
