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
            "history"
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
                self.set_filter("ALL")
        )


        self.victory_button = MDRaisedButton(
            on_release=lambda x:
                self.set_filter("Victory")
        )


        self.defeat_button = MDRaisedButton(
            on_release=lambda x:
                self.set_filter("Defeat")
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

        # --------------------------------------------
        # Filter buttons
        # --------------------------------------------

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

        self.current_filter = filter_value

        self.update_filter_colors()

        self.refresh_history()


    def update_filter_colors(self):

        inactive = (
            self.theme_manager.get(
                "inactive_button"
            )
        )


        # --------------------------------------------
        # All inactive
        # --------------------------------------------

        self.all_button.md_bg_color = inactive

        self.victory_button.md_bg_color = inactive

        self.defeat_button.md_bg_color = inactive


        # --------------------------------------------
        # Active filter
        # --------------------------------------------

        if self.current_filter == "ALL":

            self.all_button.md_bg_color = (
                0,
                0.6,
                0,
                1,
            )


        elif self.current_filter == "Victory":

            self.victory_button.md_bg_color = (
                0,
                0.6,
                0,
                1,
            )


        elif self.current_filter == "Defeat":

            self.defeat_button.md_bg_color = (
                0.8,
                0,
                0,
                1,
            )


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
            )


            self.apply_label_theme(
                label,
                "text_secondary"
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
            style="outlined",
            line_width=dp(2),
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
        # Border depending on result
        # --------------------------------------------

        if game.result == "Victory":

            card.line_color = (
                0,
                0.7,
                0,
                1,
            )

        else:

            card.line_color = (
                0.8,
                0,
                0,
                1,
            )


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
            text=self.language_manager.get(
                "game"
            ),
            bold=True,
            adaptive_height=True,
        )


        self.apply_label_theme(
            game_label,
            "text_primary"
        )


        game_details = MDLabel(
            text=format_game(game),
            adaptive_height=True,
        )


        self.apply_label_theme(
            game_details,
            "card_text_secondary"
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


        adversary_difficulty = sum(

            get_adversary_difficulty(
                adv.adversary.id,
                adv.difficulty.id
            ).score_difficulty

            for adv in game.adversaries
        )


        scenario_difficulty = sum(

            scenario.score_difficulty

            for scenario in game.scenarios
        )


        breakdown = calculate_score_breakdown(
            result=game.result,
            scenario_difficulty=scenario_difficulty,
            adversary_difficulty=adversary_difficulty,
            players=game.players,
            invader_cards=game.invader_cards_remaining,
            dahan=game.dahan_remaining,
            blight=game.blight_remaining,
        )


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


        adversaries_text = (
            self.language_manager.get(
                "adversaries"
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


        score_text = (

            f"{result_text} +"
            f"{breakdown['victory_bonus']}\n\n"

            f"{difficulty_text}\n"

            f"   {adversaries_text}: "
            f"{adversary_difficulty} × 5\n"

            f"   {scenario_text}: "
            f"{scenario_difficulty} × 5\n\n"

            f"{final_board_text}\n"

            f"   {invader_cards_text}: "
            f"{game.invader_cards_remaining} × 2 "
            f"= +{breakdown['invader_bonus']}\n"

            f"   {dahan_text}: "
            f"{game.dahan_remaining} / "
            f"{game.players} "
            f"= +{round(breakdown['survival_bonus'])}\n"

            f"   {blight_text}: -"
            f"{game.blight_remaining} / "
            f"{game.players} "
            f"= -{round(breakdown['blight_bonus'])}\n\n"

            f"{final_score_text}: {game.score}"
        )


        score_label = MDLabel(
            text=score_text,
            adaptive_height=True,
        )


        self.apply_label_theme(
            score_label,
            "card_text_secondary"
        )


        score_summary.add_widget(
            score_label
        )


        # --------------------------------------------
        # Columns
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

        label.text_color = (
            self.theme_manager.get(
                theme_key
            )
        )