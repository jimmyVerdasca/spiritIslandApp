from .baseScreen import BaseScreen

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog

from engine.formatter import format_game
from engine.scoring import calculate_score
from database.database import finish_game, get_adversary_difficulty, get_scenario_difficulty

import kivymd
print(kivymd.__version__)


class FinishGameScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.game = None
        self.result = "Victory"

        layout = MDBoxLayout(
            orientation="vertical",
            padding="10dp",
            spacing="10dp",
        )

        self.add_top_bar(
            layout,
            "Finish Game"
        )

        scroll = MDScrollView()

        self.card = MDCard(
            orientation="vertical",
            padding="20dp",
            spacing="15dp",
            adaptive_height=True,
        )

        self.game_label = MDLabel(
            halign="left",
            valign="top",
            size_hint_y=None,
            adaptive_height=True,
        )

        self.card.add_widget(self.game_label)

        # -----------------------------
        # Victory / Defeat selector
        # -----------------------------

        self.result = "Victory"

        result_box = MDBoxLayout(
            orientation="horizontal",
            spacing="10dp",
            size_hint_y=None,
            height="50dp"
        )

        self.victory_button = MDRaisedButton(
            text="Victory",
            on_release=lambda x: self.set_result("Victory")
        )

        self.defeat_button = MDRaisedButton(
            text="Defeat",
            on_release=lambda x: self.set_result("Defeat")
        )

        result_box.add_widget(self.victory_button)
        result_box.add_widget(self.defeat_button)

        self.card.add_widget(result_box)

        # -----------------------------
        # Score inputs
        # -----------------------------

        self.invader_cards = MDTextField(
            hint_text="Invader cards remaining",
            input_filter="int",
        )

        self.card.add_widget(self.invader_cards)

        self.dahan = MDTextField(
            hint_text="Dahan remaining",
            input_filter="int",
        )

        self.card.add_widget(self.dahan)

        self.blight = MDTextField(
            hint_text="Blight on island",
            input_filter="int",
        )

        self.card.add_widget(self.blight)

        self.invader_cards.bind(
            text=self.update_preview
        )

        self.dahan.bind(
            text=self.update_preview
        )

        self.blight.bind(
            text=self.update_preview
        )

        self.score_label = MDLabel(
            text="Score preview: -",
            halign="center",
            adaptive_height=True,
        )

        self.card.add_widget(self.score_label)


        self.save_button = MDRaisedButton(
            text="Save Result",
            disabled=True,
            on_release=self.save_result,
        )

        self.card.add_widget(self.save_button)

        scroll.add_widget(self.card)
        layout.add_widget(scroll)

        self.add_widget(layout)

        self.set_result("Victory")

    def load_game(self, game):

        self.game = game

        self.game_label.text = format_game(game)

    def save_result(self, *args):
    
        if self.game is None:
            return


        invader_cards = int(
            self.invader_cards.text or 0
        )

        dahan = int(
            self.dahan.text or 0
        )

        blight = int(
            self.blight.text or 0
        )

        adversary_difficulty = 0
        for adv in self.game.adversaries:
            adversary_difficulty += get_adversary_difficulty(
                adv.adversary.id,
                adv.difficulty.id
            ).score_difficulty

        scenario_difficulty = 0
        for scenario in self.game.scenarios:
            scenario_difficulty += get_scenario_difficulty(
                scenario.id
            )


        score = calculate_score(
            result=self.result,
            scenario_difficulty=scenario_difficulty,
            adversary_difficulty=adversary_difficulty,
            players=self.game.players,
            invader_cards=invader_cards,
            dahan=dahan,
            blight=blight
        )


        finish_game(
            game_id=self.game.id,
            result=self.result,
            score=score,
            invader_cards=invader_cards,
            dahan=dahan,
            blight=blight
        )


        self.show_saved_dialog(score)

    def set_result(self, result):
    
        self.result = result

        if result == "Victory":

            self.victory_button.md_bg_color = (
                0,
                0.6,
                0,
                1
            )

            self.defeat_button.md_bg_color = (
                0.8,
                0.8,
                0.8,
                1
            )

        else:

            self.defeat_button.md_bg_color = (
                0.8,
                0,
                0,
                1
            )

            self.victory_button.md_bg_color = (
                0.8,
                0.8,
                0.8,
                1
            )

    def on_pre_enter(self):
    
        if self.game:
            self.game_label.text = format_game(self.game)

    def update_preview(self, *args):
    
        filled = all([
            self.invader_cards.text,
            self.dahan.text,
            self.blight.text,
        ])

        self.save_button.disabled = not filled

        if not filled or self.game is None:
            self.score_label.text = "Score preview: -"
            return


        invader_cards = int(self.invader_cards.text)
        dahan = int(self.dahan.text)
        blight = int(self.blight.text)


        adversary_difficulty = 0

        for adv in self.game.adversaries:
            adversary_difficulty += get_adversary_difficulty(
                adv.adversary.id,
                adv.difficulty.id
            ).score_difficulty


        scenario_difficulty = 0

        for scenario in self.game.scenarios:
            scenario_difficulty += get_scenario_difficulty(
                scenario.id
            )


        score = calculate_score(
            result=self.result,
            scenario_difficulty=scenario_difficulty,
            adversary_difficulty=adversary_difficulty,
            players=self.game.players,
            invader_cards=invader_cards,
            dahan=dahan,
            blight=blight
        )


        self.score_label.text = f"Score preview: {score}"

    def show_saved_dialog(self, score):
    
        self.dialog = MDDialog(
            title="Game saved",
            text=f"""
                Result: {self.result}
                Score: {score}

                Your game has been recorded.
                """,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=self.close_dialog
                )
            ],
        )

        self.dialog.open()


    def close_dialog(self, *args):

        self.dialog.dismiss()
        self.manager.current = "current"
