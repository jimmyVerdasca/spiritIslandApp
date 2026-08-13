from .baseScreen import BaseScreen

from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog

from kivy.metrics import dp

from engine.formatter import format_game
from engine.scoring import calculate_score

from database.database import (
    finish_game,
    get_adversary_difficulty,
)


class FinishGameScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # --------------------------------------------
        # Managers
        # --------------------------------------------

        app = MDApp.get_running_app()

        self.settings_manager = app.settings_manager
        self.language_manager = app.language_manager
        self.theme_manager = app.theme_manager

        # --------------------------------------------
        # State
        # --------------------------------------------

        self.game = None
        self.result = "Victory"
        self.origin_screen = "current"

        # --------------------------------------------
        # Main layout
        # --------------------------------------------

        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
        )

        self.add_top_bar(
            layout,
            "finish_game",
        )

        # --------------------------------------------
        # Scroll
        # --------------------------------------------

        scroll = MDScrollView()

        self.card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            adaptive_height=True,
            radius=[dp(20)],
        )

        # --------------------------------------------
        # Game information
        # --------------------------------------------

        self.game_label = MDLabel(
            halign="left",
            valign="top",
            size_hint_y=None,
            adaptive_height=True,
        )

        self.game_label.bind(
            texture_size=self.game_label.setter(
                "size"
            )
        )

        self.card.add_widget(
            self.game_label
        )

        # --------------------------------------------
        # Result selector
        # --------------------------------------------

        self.build_result_selector()

        # --------------------------------------------
        # Score inputs
        # --------------------------------------------

        self.build_score_inputs()

        # --------------------------------------------
        # Score preview
        # --------------------------------------------

        self.score_label = MDLabel(
            halign="center",
            adaptive_height=True,
        )

        self.card.add_widget(
            self.score_label
        )

        # --------------------------------------------
        # Save button
        # --------------------------------------------

        self.save_button = MDRaisedButton(
            disabled=True,
            on_release=self.save_result,
        )

        self.card.add_widget(
            self.save_button
        )

        scroll.add_widget(
            self.card
        )

        layout.add_widget(
            scroll
        )

        self.add_widget(
            layout
        )

        # --------------------------------------------
        # Initial state
        # --------------------------------------------

        self.set_result("Victory")

        self.refresh_ui()

    # ====================================================
    # Lifecycle
    # ====================================================

    def on_pre_enter(self):

        self.refresh_ui()

        if self.game:

            self.game_label.text = format_game(
                self.game
            )

        else:

            self.game_label.text = ""

        self.update_preview()

    # ====================================================
    # UI refresh
    # ====================================================

    def refresh_ui(self):

        self.update_text()
        self.update_theme()

    # ====================================================
    # Translation
    # ====================================================

    def update_text(self):

        if not hasattr(self, "top_bar_title"):
            return

        self.top_bar_title.text = (
            self.language_manager.get(
                "finish_game"
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

        self.invader_cards.hint_text = (
            self.language_manager.get(
                "invader_cards_remaining"
            )
        )

        self.dahan.hint_text = (
            self.language_manager.get(
                "dahan_remaining"
            )
        )

        self.blight.hint_text = (
            self.language_manager.get(
                "blight_on_island"
            )
        )

        self.save_button.text = (
            self.language_manager.get(
                "save_result"
            )
        )

        self.update_preview()

    # ====================================================
    # Theme
    # ====================================================

    def update_theme(self):

        self.card.md_bg_color = (
            self.theme_manager.get(
                "card"
            )
        )

        self.game_label.theme_text_color = "Custom"

        self.game_label.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )

        self.score_label.theme_text_color = "Custom"

        self.score_label.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )

        self.invader_cards.theme_text_color = "Custom"

        self.invader_cards.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )

        self.dahan.theme_text_color = "Custom"

        self.dahan.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )

        self.blight.theme_text_color = "Custom"

        self.blight.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )

        self.update_result_colors()

    # ====================================================
    # Result selector
    # ====================================================

    def build_result_selector(self):

        box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50),
        )

        self.victory_button = MDRaisedButton(
            on_release=lambda x:
            self.set_result("Victory"),
        )

        self.defeat_button = MDRaisedButton(
            on_release=lambda x:
            self.set_result("Defeat"),
        )

        box.add_widget(
            self.victory_button
        )

        box.add_widget(
            self.defeat_button
        )

        self.card.add_widget(
            box
        )

    # ====================================================
    # Score inputs
    # ====================================================

    def build_score_inputs(self):

        self.invader_cards = self.create_input(
            "invader_cards_remaining"
        )

        self.dahan = self.create_input(
            "dahan_remaining"
        )

        self.blight = self.create_input(
            "blight_on_island"
        )

        for field in (
            self.invader_cards,
            self.dahan,
            self.blight,
        ):

            field.bind(
                text=self.update_preview
            )

            self.card.add_widget(
                field
            )

    def create_input(self, translation_key):

        return MDTextField(
            hint_text=self.language_manager.get(
                translation_key
            ),
            input_filter="int",
        )

    # ====================================================
    # Game loading
    # ====================================================

    def load_game(
        self,
        game,
        origin_screen="current",
    ):

        self.game = game
        self.origin_screen = origin_screen

        self.game_label.text = format_game(
            game
        )

        self.update_preview()

    # ====================================================
    # Difficulties
    # ====================================================

    def get_difficulties(self):

        if not self.game:
            return 0, 0

        adversary_difficulty = 0

        for game_adversary in self.game.adversaries:

            if game_adversary.difficulty is None:
                continue

            result = get_adversary_difficulty(
                game_adversary.adversary.id,
                game_adversary.difficulty.id,
            )

            if result:

                adversary_difficulty += (
                    result.score_difficulty
                )

        scenario_difficulty = sum(
            scenario.score_difficulty
            for scenario in self.game.scenarios
        )

        return (
            adversary_difficulty,
            scenario_difficulty,
        )

    # ====================================================
    # Input values
    # ====================================================

    def get_input_values(self):

        try:

            invader_cards = int(
                self.invader_cards.text
            )

            dahan = int(
                self.dahan.text
            )

            blight = int(
                self.blight.text
            )

        except (TypeError, ValueError):

            return None

        if (
            invader_cards < 0
            or dahan < 0
            or blight < 0
        ):

            return None

        return (
            invader_cards,
            dahan,
            blight,
        )

    # ====================================================
    # Score
    # ====================================================

    def calculate_current_score(self):

        if not self.game:
            return None

        values = self.get_input_values()

        if values is None:
            return None

        (
            invader_cards,
            dahan,
            blight,
        ) = values

        adversary, scenario = (
            self.get_difficulties()
        )

        return calculate_score(
            result=self.result,
            scenario_difficulty=scenario,
            adversary_difficulty=adversary,
            players=self.game.players,
            invader_cards=invader_cards,
            dahan=dahan,
            blight=blight,
        )

    # ====================================================
    # Result
    # ====================================================

    def set_result(self, result):

        if result not in (
            "Victory",
            "Defeat",
        ):
            return

        self.result = result

        self.update_result_colors()
        self.update_preview()

    def update_result_colors(self):

        if not hasattr(
            self,
            "victory_button",
        ):
            return

        inactive = (
            self.theme_manager.get(
                "inactive_button"
            )
        )

        success = (
            self.theme_manager.get(
                "button"
            )
        )

        defeat = (
            self.theme_manager.get(
                "defeat"
            )
        )

        if self.result == "Victory":

            self.victory_button.md_bg_color = (
                success
            )

            self.defeat_button.md_bg_color = (
                inactive
            )

        else:

            self.defeat_button.md_bg_color = (
                defeat
            )

            self.victory_button.md_bg_color = (
                inactive
            )

    # ====================================================
    # Score preview
    # ====================================================

    def update_preview(self, *args):

        if not self.game:

            self.save_button.disabled = True

            self.score_label.text = (
                self.language_manager.get(
                    "score_preview"
                )
                + ": -"
            )

            return

        score = self.calculate_current_score()

        self.save_button.disabled = (
            score is None
        )

        if score is None:

            self.score_label.text = (
                self.language_manager.get(
                    "score_preview"
                )
                + ": -"
            )

            return

        self.score_label.text = (
            self.language_manager.get(
                "score_preview"
            )
            + f": {score}"
        )

    # ====================================================
    # Save
    # ====================================================

    def save_result(self, *args):

        if not self.game:
            return

        values = self.get_input_values()

        if values is None:
            return

        (
            invader_cards,
            dahan,
            blight,
        ) = values

        score = self.calculate_current_score()

        if score is None:
            return

        finish_game(
            game_id=self.game.id,
            result=self.result,
            score=score,
            invader_cards=invader_cards,
            dahan=dahan,
            blight=blight,
        )

        self.show_saved_dialog(
            score
        )

    # ====================================================
    # Dialog
    # ====================================================

    def show_saved_dialog(self, score):

        result_text = (
            self.language_manager.get(
                "victory"
            )
            if self.result == "Victory"
            else
            self.language_manager.get(
                "defeat"
            )
        )

        self.dialog = MDDialog(

            title=self.language_manager.get(
                "game_saved"
            ),

            text=(
                f"{self.language_manager.get('result')}: "
                f"{result_text}\n"
                f"{self.language_manager.get('score')}: "
                f"{score}\n\n"
                f"{self.language_manager.get('game_recorded')}"
            ),

            buttons=[

                MDRaisedButton(
                    text=self.language_manager.get(
                        "ok"
                    ),
                    on_release=self.close_dialog,
                ),

            ],
        )

        self.dialog.open()

    def close_dialog(self, *args):

        self.dialog.dismiss()

        self.navigate_to(
            self.origin_screen,
            previous="home",
        )