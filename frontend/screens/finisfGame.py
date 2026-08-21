from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from shared.engine.formatter import format_game
from shared.engine.scoring import calculate_score

from .baseScreen import BaseScreen

class FinishGameScreen(BaseScreen):

    """
    Finish a running game and record its result.

    Responsibilities:

        - Load the selected game.
        - Select Victory / Defeat.
        - Collect final board values.
        - Calculate the score.
        - Save the completed game.
        - Navigate back to the originating screen.

    Shared widget creation, theme handling, dimensions,
    typography, and top-bar behavior are provided by
    BaseScreen / WidgetFactory.
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # ====================================================
        # State
        # ====================================================

        self.game = None

        self.result = "Victory"

        self.origin_screen = "current"


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
            "finish_game",
        )


        # ====================================================
        # Scroll
        # ====================================================

        self.scroll = MDScrollView()


        self.card = self.create_card(

            orientation="vertical",

            adaptive_height=True,

            padding=self.dimension(
                "card",
                "padding",
            ),

            spacing=self.spacing(
                "sm"
            ),
        )


        self.scroll.add_widget(
            self.card
        )


        self.layout.add_widget(
            self.scroll
        )


        self.add_widget(
            self.layout
        )


        # ====================================================
        # Game information
        # ====================================================

        self.game_label = self.create_label(

            style="body",

            color="text_primary",

            halign="left",

            valign="top",

            size_hint_y=None,
        )


        self.game_label.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )


        self.card.add_widget(
            self.game_label
        )


        # ====================================================
        # Result selector
        # ====================================================

        self.build_result_selector()


        # ====================================================
        # Score inputs
        # ====================================================

        self.build_score_inputs()


        # ====================================================
        # Score preview
        # ====================================================

        self.score_label = self.create_label(

            style="body",

            color="text_primary",

            halign="center",

            size_hint_y=None,
        )


        self.score_label.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )


        self.card.add_widget(
            self.score_label
        )


        # ====================================================
        # Save button
        # ====================================================

        self.save_button = self.create_button(

            text="",

            background_color="button",

            text_color="text_primary",

            disabled=True,

            on_release=self.save_result,
        )


        self.card.add_widget(
            self.save_button
        )


        # ====================================================
        # Initial state
        # ====================================================

        self.set_result(
            "Victory"
        )

        self.refresh_ui()


    # ====================================================
    # Lifecycle
    # ====================================================

    def on_pre_enter(self):

        super().on_pre_enter()

        self.refresh_ui()


        if self.game:

            self.game_label.text = (
                format_game(
                    self.game
                )
            )

        else:

            self.game_label.text = ""


        self.update_preview()


    # ====================================================
    # UI refresh
    # ====================================================

    def refresh_ui(self):

        self.update_text()

        self.update_result_colors()


    # ====================================================
    # Translation
    # ====================================================

    def update_text(self):

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

    def refresh_screen_theme(self):

        self.update_result_colors()


    # ====================================================
    # Result selector
    # ====================================================

    def build_result_selector(self):

        box = MDBoxLayout(

            orientation="horizontal",

            spacing=self.spacing(
                "sm"
            ),

            size_hint_y=None,

            height=self.dimension(
                "button",
                "height",
            ),
        )


        self.victory_button = self.create_button(

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_result(
                "Victory"
            ),
        )


        self.defeat_button = self.create_button(

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_result(
                "Defeat"
            ),
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


    def create_input(
        self,
        translation_key,
    ):

        return super().create_input(
            hint_text=self.language_manager.get(
                translation_key
            ),

            text_color="text_primary",
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

        self.origin_screen = (
            origin_screen
        )


        self.game_label.text = (
            format_game(
                game
            )
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

            key = (
                game_adversary.adversary.id,
                game_adversary.difficulty.id,
            )

            score_difficulty = (
                self.data.adversaries_difficulties.get(key)
            )

            if score_difficulty is not None:
                adversary_difficulty += score_difficulty

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

        except (
            TypeError,
            ValueError,
        ):

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

    def set_result(
        self,
        result,
    ):

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


        self.apply_button_theme(

            self.victory_button,

            background_color=(
                "button"
                if self.result == "Victory"
                else "inactive_button"
            ),

            text_color="text_primary",
        )


        self.apply_button_theme(

            self.defeat_button,

            background_color=(
                "defeat"
                if self.result == "Defeat"
                else "inactive_button"
            ),

            text_color="text_primary",
        )


    # ====================================================
    # Score preview
    # ====================================================

    def update_preview(
        self,
        *args,
    ):

        if not self.game:

            self.save_button.disabled = True

            self.score_label.text = (

                self.language_manager.get(
                    "score_preview"
                )

                + ": -"
            )

            return


        score = (
            self.calculate_current_score()
        )


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

    def save_result(
        self,
        *args,
    ):

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


        score = (
            self.calculate_current_score()
        )


        if score is None:

            return


        self.data.finish_game(

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

    def show_saved_dialog(
        self,
        score,
    ):

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


    def close_dialog(
        self,
        *args,
    ):

        self.dialog.dismiss()


        self.navigate_to(
            self.origin_screen,
            previous="home",
        )