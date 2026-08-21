from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView

from .widgets.history_card import HistoryCard
from .baseScreen import BaseScreen


class HistoryScreen(BaseScreen):

    """
    Display completed games and their score breakdowns.
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        # ====================================================
        # State
        # ====================================================

        self.current_filter = "ALL"


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
            "history",
        )


        # ====================================================
        # Filters
        # ====================================================

        self.filter_box = MDBoxLayout(

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


        self.all_button = self.create_button(

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_filter("ALL"),
        )


        self.victory_button = self.create_button(

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_filter("Victory"),
        )


        self.defeat_button = self.create_button(

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_filter("Defeat"),
        )


        self.filter_box.add_widget(
            self.all_button
        )

        self.filter_box.add_widget(
            self.victory_button
        )

        self.filter_box.add_widget(
            self.defeat_button
        )


        self.layout.add_widget(
            self.filter_box
        )


        # ====================================================
        # Scroll area
        # ====================================================

        self.scroll = MDScrollView()


        self.container = MDBoxLayout(

            orientation="vertical",

            adaptive_height=True,

            spacing=self.spacing(
                "sm"
            ),
        )


        self.scroll.add_widget(
            self.container
        )


        self.layout.add_widget(
            self.scroll
        )


        # ====================================================
        # Add screen
        # ====================================================

        self.add_widget(
            self.layout
        )


        # ====================================================
        # Initial UI
        # ====================================================

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

        self.update_filter_colors()

        self.refresh_history()


    # ====================================================
    # Translation
    # ====================================================

    def update_text(self):

        self.all_button.text = str(
            self.language_manager.get(
                "all"
            )
        )


        self.victory_button.text = str(
            self.language_manager.get(
                "victory"
            )
        )


        self.defeat_button.text = str(
            self.language_manager.get(
                "defeat"
            )
        )


    # ====================================================
    # Theme
    # ====================================================

    def refresh_screen_theme(self):

        self.update_filter_colors()

        self.refresh_history()


    # ====================================================
    # Filters
    # ====================================================

    def set_filter(
        self,
        filter_value,
    ):

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

        buttons = {

            "ALL": self.all_button,

            "Victory": self.victory_button,

            "Defeat": self.defeat_button,
        }


        # ------------------------------------------------
        # Inactive buttons
        # ------------------------------------------------

        for button in buttons.values():

            self.apply_button_theme(

                button,

                background_color="inactive_button",

                text_color="text_primary",
            )


        # ------------------------------------------------
        # Active button
        # ------------------------------------------------

        active_button = buttons.get(
            self.current_filter
        )


        if active_button is not None:

            self.apply_button_theme(

                active_button,

                background_color="button",

                text_color="text_primary",
            )


    # ====================================================
    # History loading
    # ====================================================

    def refresh_history(self):

        self.container.clear_widgets()


        # ------------------------------------------------
        # Get games
        # ------------------------------------------------

        if self.current_filter == "ALL":

            games = self.data.get_finished_games()

        else:

            games = self.data.get_finished_games(
                result=self.current_filter
            )


        # ------------------------------------------------
        # Empty state
        # ------------------------------------------------

        if not games:

            label = self.create_label(

                text=str(
                    self.language_manager.get(
                        "no_completed_games"
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


            self.container.add_widget(
                label
            )

            return


        # ------------------------------------------------
        # Game cards
        # ------------------------------------------------

        for game in games:

            card = HistoryCard(

                game=game,

                widget_factory=self.widget_factory,

                theme=self.theme,

                language_manager=self.language_manager,
            )


            self.container.add_widget(
                card
            )
