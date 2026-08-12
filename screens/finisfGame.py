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
            "finish_game"
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

        self.set_result(
            "Victory"
        )

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

        # Top bar title

        self.top_bar_title.text = (
            self.language_manager.get(
                "finish_game"
            )
        )


        # Result buttons

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


        # Input hints

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


        # Save button

        self.save_button.text = (
            self.language_manager.get(
                "save_result"
            )
        )


        # Score preview

        if not self.game:

            self.score_label.text = (
                self.language_manager.get(
                    "score_preview"
                ) + ": -"
            )


    # ====================================================
    # Theme
    # ====================================================

    def update_theme(self):

        # --------------------------------------------
        # Card
        # --------------------------------------------

        self.card.md_bg_color = (
            self.theme_manager.get(
                "card"
            )
        )


        # --------------------------------------------
        # Game information
        # --------------------------------------------

        self.game_label.theme_text_color = "Custom"

        self.game_label.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )


        # --------------------------------------------
        # Score preview
        # --------------------------------------------

        self.score_label.theme_text_color = "Custom"

        self.score_label.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )


        # --------------------------------------------
        # Inputs
        # --------------------------------------------

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


        # --------------------------------------------
        # Result buttons
        # --------------------------------------------

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
            self.set_result("Victory")
        )


        self.defeat_button = MDRaisedButton(
            on_release=lambda x:
            self.set_result("Defeat")
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


        for field in [
            self.invader_cards,
            self.dahan,
            self.blight,
        ]:

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

    def load_game(self, game):

        self.game = game

        self.game_label.text = format_game(
            game
        )

        self.update_preview()


    # ====================================================
    # Difficulties
    # ====================================================

    def get_difficulties(self):

        adversary = 0


        for adv in self.game.adversaries:

            result = get_adversary_difficulty(
                adv.adversary.id,
                adv.difficulty.id
            )


            if result:

                adversary += (
                    result.score_difficulty
                )


        scenario = sum(
            s.score_difficulty
            for s in self.game.scenarios
        )


        return adversary, scenario


    # ====================================================
    # Score
    # ====================================================

    def calculate_current_score(self):

        invader_cards = int(
            self.invader_cards.text
        )

        dahan = int(
            self.dahan.text
        )

        blight = int(
            self.blight.text
        )


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
            blight=blight
        )


    # ====================================================
    # Result
    # ====================================================

    def set_result(self, result):

        self.result = result

        self.update_result_colors()


    def update_result_colors(self):

        if not hasattr(
            self,
            "victory_button"
        ):
            return


        inactive = (
            self.theme_manager.get(
                "inactive_button"
            )
        )


        if self.result == "Victory":

            self.victory_button.md_bg_color = (
                0,
                0.6,
                0,
                1
            )

            self.defeat_button.md_bg_color = (
                inactive
            )

        else:

            self.defeat_button.md_bg_color = (
                0.8,
                0,
                0,
                1
            )

            self.victory_button.md_bg_color = (
                inactive
            )


    # ====================================================
    # Score preview
    # ====================================================

    def update_preview(self, *args):

        filled = all([
            self.invader_cards.text,
            self.dahan.text,
            self.blight.text,
        ])


        self.save_button.disabled = not filled


        if not filled or not self.game:

            self.score_label.text = (
                self.language_manager.get(
                    "score_preview"
                )
                + ": -"
            )

            return


        score = self.calculate_current_score()


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


        score = self.calculate_current_score()


        finish_game(
            game_id=self.game.id,
            result=self.result,
            score=score,
            invader_cards=int(
                self.invader_cards.text
            ),
            dahan=int(
                self.dahan.text
            ),
            blight=int(
                self.blight.text
            )
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
                    on_release=self.close_dialog
                )

            ],
        )


        self.dialog.open()


    def close_dialog(self, *args):

        self.dialog.dismiss()

        self.navigate_to(
            "current",
            previous="home"
        )