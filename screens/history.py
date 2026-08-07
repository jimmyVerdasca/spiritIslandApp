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

        self.current_filter = "ALL"

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20),
        )


        self.add_top_bar(
            layout,
            "History"
        )


        # ---------------------------------
        # Filters
        # ---------------------------------

        filter_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )


        self.all_button = MDRaisedButton(
            text="All",
            on_release=lambda x: self.set_filter("ALL")
        )

        self.victory_button = MDRaisedButton(
            text="Victory",
            on_release=lambda x: self.set_filter("Victory")
        )

        self.defeat_button = MDRaisedButton(
            text="Defeat",
            on_release=lambda x: self.set_filter("Defeat")
        )


        filter_box.add_widget(self.all_button)
        filter_box.add_widget(self.victory_button)
        filter_box.add_widget(self.defeat_button)


        layout.add_widget(filter_box)


        # ---------------------------------
        # Scroll area
        # ---------------------------------

        scroll = MDScrollView()


        self.container = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(10),
        )


        scroll.add_widget(
            self.container
        )

        layout.add_widget(scroll)


        self.add_widget(layout)


        # Apply initial filter colors
        self.update_filter_colors()



    def on_enter(self):

        self.refresh_history()



    # ---------------------------------
    # Filters
    # ---------------------------------

    def set_filter(self, filter_value):

        self.current_filter = filter_value

        self.update_filter_colors()

        self.refresh_history()



    def update_filter_colors(self):

        grey = (
            0.8,
            0.8,
            0.8,
            1
        )

        self.all_button.md_bg_color = grey
        self.victory_button.md_bg_color = grey
        self.defeat_button.md_bg_color = grey


        if self.current_filter == "ALL":

            self.all_button.md_bg_color = (
                0,
                0.6,
                0,
                1
            )


        elif self.current_filter == "Victory":

            self.victory_button.md_bg_color = (
                0,
                0.6,
                0,
                1
            )


        elif self.current_filter == "Defeat":

            self.defeat_button.md_bg_color = (
                0.8,
                0,
                0,
                1
            )



    # ---------------------------------
    # History loading
    # ---------------------------------

    def refresh_history(self):

        self.container.clear_widgets()


        if self.current_filter == "ALL":

            games = get_finished_games()

        else:

            games = get_finished_games(
                result=self.current_filter
            )


        if not games:

            self.container.add_widget(
                MDLabel(
                    text="No completed games.",
                    adaptive_height=True,
                )
            )

            return


        for game in games:

            self.container.add_widget(
                self.build_game_card(game)
            )



    # ---------------------------------
    # Game card
    # ---------------------------------

    def build_game_card(self, game):

        card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            adaptive_height=True,
            style="outlined",
            line_width=dp(2),
        )


        # Border depending on result

        if game.result == "Victory":

            card.line_color = (
                0,
                0.7,
                0,
                1
            )

        else:

            card.line_color = (
                0.8,
                0,
                0,
                1
            )



        columns = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            adaptive_height=True,
        )


        # ---------------------------------
        # Left side: game description
        # ---------------------------------

        game_summary = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(5),
        )


        game_summary.add_widget(
            MDLabel(
                text="Game",
                bold=True,
                adaptive_height=True,
            )
        )


        game_summary.add_widget(
            MDLabel(
                text=format_game(game),
                adaptive_height=True,
            )
        )



        # ---------------------------------
        # Right side: score computation
        # ---------------------------------

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
            blight=game.blight_remaining
        )


        score_summary.add_widget(
            MDLabel(
                text=(
                    f"{game.result} +{breakdown['victory_bonus']}\n\n"

                    "Difficulty\n"
                    f"   Adversaries: {adversary_difficulty} × 5\n"
                    f"   Scenario: {scenario_difficulty} × 5\n\n"


                    "Final board state\n"
                    f"   Invader cards: {game.invader_cards_remaining} × 2 = +{breakdown['invader_bonus']}\n"
                    f"   Dahan: {game.dahan_remaining} / {game.players}  = +{round(breakdown['survival_bonus'])}\n"
                    f"   Blight: -{game.blight_remaining} / {game.players}  = -{round(breakdown['blight_bonus'])}\n\n"

                    f"FINAL SCORE: {game.score}"
                ),
                adaptive_height=True,
            )
        )

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