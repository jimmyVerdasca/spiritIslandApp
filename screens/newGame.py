from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog


from .baseScreen import BaseScreen


from engine.generator import generate_game
from engine.formatter import format_game
from widgets.section_header import SectionHeader
from widgets.player_card import PlayerCard
from widgets.selection_row import SelectionRow
from widgets.section_header import SectionHeader

class NewGameScreen(BaseScreen):

    def __init__(
        self,
        **kwargs,
    ):

        super().__init__(
            **kwargs
        )


        # =================================================
        # State
        # =================================================

        self.players = None
        self.configuration = None

        self.player_rows = []
        self.adversary_rows = []
        self.scenario_rows = []

        self.configuration_menu = None
        self.players_menu = None
        self.adversary_menu = None
        self.level_menu = None
        self.scenario_menu = None
        self.spirit_menu = None
        self.board_menu = None
        self.help_dialog = None


        # =================================================
        # Main layout
        # =================================================

        root = MDBoxLayout(
            orientation="vertical",
        )


        # =================================================
        # Top bar
        # =================================================

        self.add_top_bar(
            root,
            "new_game",
        )


        # =================================================
        # Scroll content
        # =================================================

        scroll = MDScrollView()


        content = MDBoxLayout(
            orientation="vertical",
            spacing=self.spacing("lg"),
            padding=self.spacing("lg"),
            adaptive_height=True,
        )


        # =================================================
        # Configuration
        # =================================================

        self.add_section_title(
            content,
            self.t("configuration"),
            self.t("configuration_description"),
        )


        self.configuration_button = (
            self.create_button(
                text=self.t("any"),
            )
        )


        self.configuration_button.bind(
            on_release=self.open_configuration_menu
        )


        content.add_widget(
            self.configuration_button
        )


        # =================================================
        # Players
        # =================================================

        self.add_section_title(
            content,
            self.t("players"),
            self.t("players_description"),
        )


        self.players_button = (
            self.create_button(
                text=self.t("any"),
            )
        )


        self.players_button.bind(
            on_release=self.open_players_menu
        )


        content.add_widget(
            self.players_button
        )


        # =================================================
        # Player cards
        # =================================================

        self.players_container = MDBoxLayout(
            orientation="vertical",
            spacing=self.spacing("md"),
            adaptive_height=True,
        )


        content.add_widget(
            self.players_container
        )


        # =================================================
        # Adversaries
        # =================================================

        self.add_section_title(
            content,
            self.adversaries_title(),
            self.t("adversaries_description"),
        )


        self.add_adversary_button = (
            self.create_button(
                text=self.t("add_adversary"),
            )
        )


        self.add_adversary_button.bind(
            on_release=self.add_adversary_row
        )


        content.add_widget(
            self.add_adversary_button
        )


        self.adversaries_container = MDBoxLayout(
            orientation="vertical",
            spacing=self.spacing("sm"),
            adaptive_height=True,
        )


        content.add_widget(
            self.adversaries_container
        )


        # =================================================
        # Scenarios
        # =================================================

        self.add_section_title(
            content,
            self.t("scenario"),
            self.t("scenarios_description"),
        )


        self.add_scenario_button = (
            self.create_button(
                text=self.t("add_scenario"),
            )
        )


        self.add_scenario_button.bind(
            on_release=self.add_scenario_row
        )


        content.add_widget(
            self.add_scenario_button
        )


        self.scenarios_container = MDBoxLayout(
            orientation="vertical",
            spacing=self.spacing("sm"),
            adaptive_height=True,
        )


        content.add_widget(
            self.scenarios_container
        )


        # =================================================
        # Generate
        # =================================================

        self.generate_button = (
            self.create_button(
                text=self.t("generate"),
            )
        )


        self.generate_button.pos_hint = {
            "center_x": 0.5,
        }


        self.generate_button.bind(
            on_release=self.generate
        )


        content.add_widget(
            self.generate_button
        )


        # =================================================
        # Result card
        # =================================================

        self.result_card = self.create_card(
            adaptive_height=True,
            background_color="card",
            orientation="vertical",
        )


        self.result = self.create_label(
            text=self.t("press_generate"),
            style="secondary",
            color="card_text_secondary",
            size_hint_y=None,
            adaptive_height=True,
        )


        self.result_card.add_widget(
            self.result
        )


        content.add_widget(
            self.result_card
        )


        # =================================================
        # Assemble
        # =================================================

        scroll.add_widget(
            content
        )

        root.add_widget(
            scroll
        )

        self.add_widget(
            root
        )


        # =================================================
        # Initial UI
        # =================================================

        self.update_text()
        self.refresh_screen_theme()


    # ====================================================
    # Translation helper
    # ====================================================

    def t(
        self,
        key,
        *categories,
    ):

        value = self.language_manager.get(
            key,
            *categories,
        )

        if isinstance(value, str):

            return value

        return str(value)


    # ====================================================
    # Special case: adversaries
    # ====================================================

    def adversaries_title(self):

        value = self.language_manager.get(
            "adversaries"
        )

        if isinstance(value, str):

            return value


        language = getattr(
            self.language_manager,
            "current_language",
            "en",
        )


        if language == "fr":

            return "Adversaires"


        return "Adversaries"


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

        self.refresh_screen_theme()


    # ====================================================
    # Translation
    # ====================================================

    def update_text(self):

        if hasattr(
            self,
            "top_bar_title",
        ):

            self.top_bar_title.text = self.t(
                "new_game"
            )


        # ------------------------------------------------
        # Main buttons
        # ------------------------------------------------

        if self.configuration is None:

            self.configuration_button.text = (
                self.t("any")
            )

        else:

            self.configuration_button.text = (
                self.configuration_name(
                    self.configuration
                )
            )


        self.players_button.text = (
            self.t("any")
            if self.players is None
            else str(self.players)
        )


        self.add_adversary_button.text = (
            self.t("add_adversary")
        )


        self.add_scenario_button.text = (
            self.t("add_scenario")
        )


        self.generate_button.text = (
            self.t("generate")
        )


        # ------------------------------------------------
        # Existing adversary rows
        # ------------------------------------------------

        for row in self.adversary_rows:

            adversary = row["adversary"]
            level = row["level"]


            if adversary is None:

                row["adversary_button"].text = (
                    f"{self.adversaries_title()}: "
                    f"{self.t('any')}"
                )

            else:

                row["adversary_button"].text = (
                    f"{self.adversaries_title()}: "
                    f"{self.adversary_name(adversary)}"
                )


            if level is None:

                row["level_button"].text = (
                    f"{self.t('difficulty')}: "
                    f"{self.t('any')}"
                )

            else:

                row["level_button"].text = (
                    f"{self.t('difficulty')}: "
                    f"{level.level}"
                )


        # ------------------------------------------------
        # Existing scenario rows
        # ------------------------------------------------

        for row in self.scenario_rows:

            scenario = row["scenario"]


            row["scenario_button"].text = (

                f"{self.t('scenario')}: "
                f"{self.t('any')}"

                if scenario is None

                else

                (
                    f"{self.t('scenario')}: "
                    f"{self.scenario_name(scenario)}"
                )
            )


        # ------------------------------------------------
        # Existing player rows
        # ------------------------------------------------

        for index, row in enumerate(
            self.player_rows
        ):

            row["spirit_button"].text = (
                self.t("choose_spirit")
            )


            row["board_button"].text = (
                self.t("choose_board")
            )


            row["spirit_name_label"].text = (

                ""

                if row["spirit"] is None

                else

                self.spirit_name(
                    row["spirit"]
                )
            )


            row["board_name_label"].text = (

                self.t("any")

                if row["board"] is None

                else

                self.board_name(
                    row["board"]
                )
            )


            if "player_title" in row:

                row["player_title"].text = (
                    f"{self.t('player')} "
                    f"{index + 1}"
                )


        # ------------------------------------------------
        # Result
        # ------------------------------------------------

        if not self.result.text:

            self.result.text = (
                self.t("press_generate")
            )


    # ====================================================
    # Data translation helpers
    # ====================================================

    def spirit_name(
        self,
        spirit,
    ):

        return self.t(
            self.spirit_key(spirit),
            "spirits",
        )


    def adversary_name(
        self,
        adversary,
    ):

        return self.t(
            self.adversary_key(adversary),
            "adversaries",
        )


    def scenario_name(
        self,
        scenario,
    ):

        return self.t(
            self.scenario_key(scenario),
            "scenarios",
        )


    def board_name(
        self,
        board,
    ):

        return self.t(
            self.board_key(board),
            "boards",
        )


    def configuration_name(
        self,
        configuration,
    ):

        return self.t(
            self.configuration_key(
                configuration
            ),
            "board_configurations",
        )


    # ====================================================
    # Translation key helpers
    # ====================================================

    @staticmethod
    def normalize_key(
        value,
    ):

        return (
            str(value)
            .strip()
            .lower()
            .replace("'", "")
            .replace("-", "_")
            .replace(" ", "_")
        )


    def spirit_key(
        self,
        spirit,
    ):

        if hasattr(
            spirit,
            "key",
        ):

            return spirit.key


        if hasattr(
            spirit,
            "slug",
        ):

            return spirit.slug


        if hasattr(
            spirit,
            "name",
        ):

            return self.normalize_key(
                spirit.name
            )


        return str(spirit)


    def adversary_key(
        self,
        adversary,
    ):

        if hasattr(
            adversary,
            "key",
        ):

            return adversary.key


        if hasattr(
            adversary,
            "slug",
        ):

            return adversary.slug


        if hasattr(
            adversary,
            "name",
        ):

            return self.normalize_key(
                adversary.name
            )


        return str(adversary)


    def scenario_key(
        self,
        scenario,
    ):

        if hasattr(
            scenario,
            "key",
        ):

            return scenario.key


        if hasattr(
            scenario,
            "slug",
        ):

            return scenario.slug


        if hasattr(
            scenario,
            "name",
        ):

            return self.normalize_key(
                scenario.name
            )


        return str(scenario)


    def board_key(
        self,
        board,
    ):

        if hasattr(
            board,
            "key",
        ):

            return board.key


        if hasattr(
            board,
            "slug",
        ):

            return board.slug


        if hasattr(
            board,
            "name",
        ):

            return self.normalize_key(
                board.name
            )


        return str(board)


    def configuration_key(
        self,
        configuration,
    ):

        if hasattr(
            configuration,
            "key",
        ):

            return configuration.key


        if hasattr(
            configuration,
            "slug",
        ):

            return configuration.slug


        if hasattr(
            configuration,
            "name",
        ):

            return self.normalize_key(
                configuration.name
            )


        return str(configuration)


    # ====================================================
    # Theme
    # ====================================================

    def refresh_screen_theme(self):

        self.refresh_widget_themes()


    # ====================================================
    # Players menu
    # ====================================================

    def open_players_menu(
        self,
        instance,
    ):

        if (
            self.configuration is not None
            and self.configuration.min_players
            == self.configuration.max_players
        ):

            return


        items = [
            {
                "text": self.t("any"),
                "on_release":
                    lambda:
                    self.set_players(None),
            }
        ]


        if self.configuration is None:

            minimum = 2
            maximum = 6

        else:

            minimum = (
                self.configuration.min_players
            )

            maximum = (
                self.configuration.max_players
            )


        for i in range(
            minimum,
            maximum + 1,
        ):

            items.append(
                {
                    "text": str(i),
                    "on_release":
                        lambda x=i:
                        self.set_players(x),
                }
            )


        self.players_menu = MDDropdownMenu(
            caller=self.players_button,
            items=items,
        )


        self.players_menu.open()


    # ====================================================
    # Configuration menu
    # ====================================================

    def open_configuration_menu(
        self,
        instance,
    ):

        configurations = (
            self.data.get_configurations()
        )


        items = [
            {
                "text": self.t("any"),
                "on_release":
                    lambda:
                    self.set_configuration(
                        None
                    ),
            }
        ]


        for configuration in configurations:

            items.append(
                {
                    "text":
                        self.configuration_name(
                            configuration
                        ),
                    "on_release":
                        lambda c=configuration:
                        self.set_configuration(c),
                }
            )


        self.configuration_menu = MDDropdownMenu(
            caller=self.configuration_button,
            items=items,
        )


        self.configuration_menu.open()


    # ====================================================
    # Set players
    # ====================================================

    def set_players(
        self,
        value,
    ):

        self.players = value


        self.players_button.text = (
            self.t("any")
            if value is None
            else str(value)
        )


        self.refresh_player_rows()


        if self.players_menu:

            self.players_menu.dismiss()


    # ====================================================
    # Set configuration
    # ====================================================

    def set_configuration(
        self,
        configuration,
    ):

        self.configuration = configuration


        self.configuration_button.text = (

            self.t("any")

            if configuration is None

            else

            self.configuration_name(
                configuration
            )
        )


        if configuration is None:

            self.players = None

            self.players_button.text = (
                self.t("any")
            )


        elif (
            configuration.min_players
            == configuration.max_players
        ):

            self.players = (
                configuration.min_players
            )

            self.players_button.text = str(
                configuration.min_players
            )


        elif (
            self.players is not None
            and not (
                configuration.min_players
                <= self.players
                <= configuration.max_players
            )
        ):

            self.players = None

            self.players_button.text = (
                self.t("any")
            )


        self.refresh_player_rows()


        if self.configuration_menu:

            self.configuration_menu.dismiss()


    # ====================================================
    # Adversaries
    # ====================================================

    def add_adversary_row(
        self,
        *args,
    ):

        row_widget = SelectionRow(
            widget_factory=self.widget_factory,
            theme=self.theme,

            main_text=(
                f"{self.adversaries_title()}: "
                f"{self.t('any')}"
            ),

            main_size_hint_x=0.6,

            secondary_text=(
                f"{self.t('difficulty')}: "
                f"{self.t('any')}"
            ),

            secondary_size_hint_x=0.25,

            on_main=None,
            on_secondary=None,
            on_remove=None,
        )


        self.adversaries_container.add_widget(
            row_widget
        )


        row_data = {
            "row": row_widget,
            "adversary": None,
            "level": None,

            "adversary_button":
                row_widget.main_button,

            "level_button":
                row_widget.secondary_button,

            "remove_button":
                row_widget.remove_button,
        }


        self.adversary_rows.append(
            row_data
        )


        row_widget.remove_button.bind(
            on_release=lambda x, r=row_widget:
                self.remove_adversary_row(
                    self.adversary_rows.index(
                        next(
                            item
                            for item
                            in self.adversary_rows
                            if item["row"] == r
                        )
                    )
                )
        )


        self.rebind_adversary_rows()

        self.update_adversary_button_state()


    # ====================================================
    # Rebind adversary rows
    # ====================================================

    def rebind_adversary_rows(self):

        for index, row in enumerate(
            self.adversary_rows
        ):

            row["adversary_button"].unbind(
                on_release=self.open_adversary_menu
            )

            row["level_button"].unbind(
                on_release=self.open_level_menu
            )


            row["adversary_button"].bind(
                on_release=lambda x, i=index:
                    self.open_adversary_menu(i)
            )


            row["level_button"].bind(
                on_release=lambda x, i=index:
                    self.open_level_menu(i)
            )


    # ====================================================
    # Adversary menu
    # ====================================================

    def open_adversary_menu(
        self,
        index,
    ):

        adversaries = self.data.get_adversaries()


        selected = [
            row["adversary"]

            for i, row in enumerate(
                self.adversary_rows
            )

            if (
                i != index
                and row["adversary"] is not None
            )
        ]


        items = [
            {
                "text": self.t("any"),
                "item_state": "normal",
                "viewclass":
                    "SelectionMenuItem",
                "on_release":
                    lambda:
                    self.set_adversary(
                        index,
                        None,
                    ),
            }
        ]


        for adversary in adversaries:

            if adversary in selected:

                continue


            state = (
                "selected"

                if self.adversary_rows[index][
                    "adversary"
                ] == adversary

                else

                "normal"
            )


            items.append(
                {
                    "text":
                        self.adversary_name(
                            adversary
                        ),

                    "item_state": state,

                    "viewclass":
                        "SelectionMenuItem",

                    "on_release":
                        lambda a=adversary:
                        self.set_adversary(
                            index,
                            a,
                        ),
                }
            )


        self.adversary_menu = MDDropdownMenu(
            caller=self.adversary_rows[index][
                "adversary_button"
            ],
            items=items,
        )


        self.adversary_menu.open()


    # ====================================================
    # Set adversary
    # ====================================================

    def set_adversary(
        self,
        index,
        adversary,
    ):

        self.adversary_rows[index][
            "adversary"
        ] = adversary


        self.adversary_rows[index][
            "adversary_button"
        ].text = (

            f"{self.adversaries_title()}: "
            f"{self.t('any')}"

            if adversary is None

            else

            (
                f"{self.adversaries_title()}: "
                f"{self.adversary_name(adversary)}"
            )
        )


        if self.adversary_menu:

            self.adversary_menu.dismiss()


    # ====================================================
    # Difficulty menu
    # ====================================================

    def open_level_menu(
        self,
        index,
    ):

        difficulties = self.data.get_difficulties()


        items = [
            {
                "text": self.t("any"),
                "item_state": "normal",
                "viewclass":
                    "SelectionMenuItem",
                "on_release":
                    lambda:
                    self.set_level(
                        index,
                        None,
                    ),
            }
        ]


        current = self.adversary_rows[index][
            "level"
        ]


        for difficulty in difficulties:

            state = (

                "selected"

                if (
                    current is not None
                    and current.id
                    == difficulty.id
                )

                else

                "normal"
            )


            items.append(
                {
                    "text": str(
                        difficulty.level
                    ),

                    "item_state": state,

                    "viewclass":
                        "SelectionMenuItem",

                    "on_release":
                        lambda d=difficulty:
                        self.set_level(
                            index,
                            d,
                        ),
                }
            )


        self.level_menu = MDDropdownMenu(
            caller=self.adversary_rows[index][
                "level_button"
            ],
            items=items,
        )


        self.level_menu.open()


    # ====================================================
    # Set difficulty
    # ====================================================

    def set_level(
        self,
        index,
        difficulty,
    ):

        self.adversary_rows[index][
            "level"
        ] = difficulty


        self.adversary_rows[index][
            "level_button"
        ].text = (

            f"{self.t('difficulty')}: "
            f"{self.t('any')}"

            if difficulty is None

            else

            (
                f"{self.t('difficulty')}: "
                f"{difficulty.level}"
            )
        )


        if self.level_menu:

            self.level_menu.dismiss()


    # ====================================================
    # Remove adversary
    # ====================================================

    def remove_adversary_row(
        self,
        index,
    ):

        if (
            index < 0
            or index >= len(
                self.adversary_rows
            )
        ):

            return


        row = self.adversary_rows.pop(
            index
        )


        self.adversaries_container.remove_widget(
            row["row"]
        )


        self.rebind_adversary_rows()

        self.update_adversary_button_state()


    # ====================================================
    # Adversary button state
    # ====================================================

    def update_adversary_button_state(
        self,
    ):

        max_adversaries = len(
            self.data.get_adversaries()
        )


        self.add_adversary_button.disabled = (
            len(self.adversary_rows)
            >= max_adversaries
        )


    # ====================================================
    # Scenarios
    # ====================================================

    def add_scenario_row(
        self,
        *args,
    ):

        row_widget = SelectionRow(
            widget_factory=self.widget_factory,
            theme=self.theme,

            main_text=(
                f"{self.t('scenario')}: "
                f"{self.t('any')}"
            ),

            main_size_hint_x=1,

            on_main=None,
            on_remove=None,
        )


        self.scenarios_container.add_widget(
            row_widget
        )


        row_data = {
            "row": row_widget,
            "scenario": None,

            "scenario_button":
                row_widget.main_button,

            "remove_button":
                row_widget.remove_button,
        }


        self.scenario_rows.append(
            row_data
        )


        row_widget.main_button.bind(
            on_release=lambda x, r=row_widget:
                self.open_scenario_menu(
                    self.scenario_rows.index(
                        next(
                            item
                            for item
                            in self.scenario_rows
                            if item["row"] == r
                        )
                    )
                )
        )


        row_widget.remove_button.bind(
            on_release=lambda x, r=row_widget:
                self.remove_scenario_row(
                    self.scenario_rows.index(
                        next(
                            item
                            for item
                            in self.scenario_rows
                            if item["row"] == r
                        )
                    )
                )
        )


        self.update_scenario_button_state()


    # ====================================================
    # Scenario menu
    # ====================================================

    def open_scenario_menu(
        self,
        index,
    ):

        scenarios = self.data.get_scenarios()


        selected = [
            row["scenario"]

            for i, row in enumerate(
                self.scenario_rows
            )

            if (
                i != index
                and row["scenario"] is not None
            )
        ]


        items = [
            {
                "text": self.t("any"),
                "item_state": "normal",
                "viewclass":
                    "SelectionMenuItem",
                "on_release":
                    lambda:
                    self.set_scenario(
                        index,
                        None,
                    ),
            }
        ]


        for scenario in scenarios:

            if scenario in selected:

                continue


            state = (

                "selected"

                if self.scenario_rows[index][
                    "scenario"
                ] == scenario

                else

                "normal"
            )


            items.append(
                {
                    "text":
                        self.scenario_name(
                            scenario
                        ),

                    "item_state": state,

                    "viewclass":
                        "SelectionMenuItem",

                    "on_release":
                        lambda s=scenario:
                        self.set_scenario(
                            index,
                            s,
                        ),
                }
            )


        self.scenario_menu = MDDropdownMenu(
            caller=self.scenario_rows[index][
                "scenario_button"
            ],
            items=items,
        )


        self.scenario_menu.open()


    # ====================================================
    # Set scenario
    # ====================================================

    def set_scenario(
        self,
        index,
        scenario,
    ):

        self.scenario_rows[index][
            "scenario"
        ] = scenario


        self.scenario_rows[index][
            "scenario_button"
        ].text = (

            f"{self.t('scenario')}: "
            f"{self.t('any')}"

            if scenario is None

            else

            (
                f"{self.t('scenario')}: "
                f"{self.scenario_name(scenario)}"
            )
        )


        if self.scenario_menu:

            self.scenario_menu.dismiss()


    # ====================================================
    # Remove scenario
    # ====================================================

    def remove_scenario_row(
        self,
        index,
    ):

        if (
            index < 0
            or index >= len(
                self.scenario_rows
            )
        ):

            return


        row = self.scenario_rows.pop(
            index
        )


        self.scenarios_container.remove_widget(
            row["row"]
        )


        self.update_scenario_button_state()


    # ====================================================
    # Scenario button state
    # ====================================================

    def update_scenario_button_state(
        self,
    ):

        max_scenarios = len(
            self.data.get_scenarios()
        )


        self.add_scenario_button.disabled = (
            len(self.scenario_rows)
            >= max_scenarios
        )


    # ====================================================
    # Player cards
    # ====================================================

    def refresh_player_rows(self):
    
        self.players_container.clear_widgets()

        self.player_rows = []

        if self.players is None:
            return

        for i in range(self.players):

            index = i

            card = PlayerCard(
                player_number=i + 1,
                widget_factory=self.widget_factory,
                theme=self.theme,
                language_manager=self.language_manager,

                on_spirit=lambda x,
                    idx=index:
                    self.open_spirit_menu(idx),

                on_board=lambda x,
                    idx=index:
                    self.open_board_menu(idx),
            )

            self.players_container.add_widget(
                card
            )

            self.player_rows.append(
                {
                    "spirit": None,
                    "board": None,

                    "card": card,

                    "spirit_button":
                        card.spirit_button,

                    "board_button":
                        card.board_button,

                    "spirit_name_label":
                        card.spirit_name_label,

                    "board_name_label":
                        card.board_name_label,

                    "player_title":
                        card.player_title,
                }
            )

        self.refresh_screen_theme()


    # ====================================================
    # Spirit menu
    # ====================================================

    def open_spirit_menu(
        self,
        index,
    ):

        spirits = self.data.get_spirits()


        items = [
            {
                "text": self.t("any_spirit"),
                "item_state": "normal",
                "viewclass":
                    "SelectionMenuItem",
                "on_release":
                    lambda:
                    self.set_spirit(
                        index,
                        None,
                    ),
            }
        ]


        for spirit in spirits:

            state = "normal"

            label = self.spirit_name(
                spirit
            )


            for i, row in enumerate(
                self.player_rows
            ):

                if (
                    i != index
                    and row["spirit"] is not None
                    and row["spirit"].id
                    == spirit.id
                ):

                    state = "warning"

                    label = (
                        f"{self.spirit_name(spirit)} "
                        f"({self.t('player')} "
                        f"{i + 1})"
                    )


                if (
                    i == index
                    and row["spirit"] is not None
                    and row["spirit"].id
                    == spirit.id
                ):

                    state = "selected"

                    label = self.spirit_name(
                        spirit
                    )


            items.append(
                {
                    "text": label,

                    "item_state": state,

                    "viewclass":
                        "SelectionMenuItem",

                    "on_release":
                        lambda s=spirit:
                        self.set_spirit(
                            index,
                            s,
                        ),
                }
            )


        self.spirit_menu = MDDropdownMenu(
            caller=self.player_rows[index][
                "spirit_button"
            ],
            items=items,
        )


        self.spirit_menu.open()


    # ====================================================
    # Set spirit
    # ====================================================

    def set_spirit(
        self,
        index,
        spirit,
    ):

        if spirit is not None:

            for i, row in enumerate(
                self.player_rows
            ):

                if (
                    i != index
                    and row["spirit"] is not None
                    and row["spirit"].id == spirit.id
                ):

                    row["spirit"] = None

                    row["card"].set_spirit(None)

        row = self.player_rows[index]

        row["spirit"] = spirit

        row["card"].set_spirit(spirit)

        if self.spirit_menu:
            self.spirit_menu.dismiss()


    # ====================================================
    # Board menu
    # ====================================================

    def open_board_menu(
        self,
        index,
    ):

        boards = self.data.get_boards()


        items = [
            {
                "text": self.t("any"),
                "item_state": "normal",
                "viewclass":
                    "SelectionMenuItem",
                "on_release":
                    lambda:
                    self.set_board(
                        index,
                        None,
                    ),
            }
        ]


        for board in boards:

            state = "normal"

            label = self.board_name(
                board
            )


            for i, row in enumerate(
                self.player_rows
            ):

                if (
                    i != index
                    and row["board"] is not None
                    and row["board"].id
                    == board.id
                ):

                    state = "warning"

                    label = (
                        f"⚠ {self.board_name(board)} "
                        f"({self.t('player')} "
                        f"{i + 1})"
                    )


                if (
                    i == index
                    and row["board"] is not None
                    and row["board"].id
                    == board.id
                ):

                    state = "selected"

                    label = (
                        f"✓ {self.board_name(board)}"
                    )


            items.append(
                {
                    "text": label,

                    "item_state": state,

                    "viewclass":
                        "SelectionMenuItem",

                    "on_release":
                        lambda b=board:
                        self.set_board(
                            index,
                            b,
                        ),
                }
            )


        self.board_menu = MDDropdownMenu(
            caller=self.player_rows[index][
                "board_button"
            ],
            items=items,
        )


        self.board_menu.open()


    # ====================================================
    # Set board
    # ====================================================

    def set_board(
        self,
        index,
        board,
    ):

        if board is not None:

            for i, row in enumerate(
                self.player_rows
            ):

                if (
                    i != index
                    and row["board"] is not None
                    and row["board"].id == board.id
                ):

                    row["board"] = None

                    row["card"].set_board(None)

        row = self.player_rows[index]

        row["board"] = board

        row["card"].set_board(board)

        if self.board_menu:
            self.board_menu.dismiss()


    # ====================================================
    # Generate
    # ====================================================

    def generate(
        self,
        instance,
    ):

        spirits = [
            row["spirit"]
            for row in self.player_rows
        ]


        boards = [
            row["board"]
            for row in self.player_rows
        ]


        adversaries = [
            (
                row["adversary"],
                row["level"],
            )

            for row in self.adversary_rows
        ]


        scenarios = None


        if self.scenario_rows:

            scenarios = [
                row["scenario"]
                for row in self.scenario_rows
            ]


        game = generate_game(
            data=self.data,
            players=self.players,
            configuration=self.configuration,
            spirits=spirits,
            boards=boards,
            adversaries=adversaries,
            scenarios=scenarios,
        )

        self.data.save_game(game)

        self.result.text = format_game(
            game
        )


        self.refresh_screen_theme()


    # ====================================================
    # Help dialog
    # ====================================================

    def show_help(
        self,
        title,
        text,
    ):

        self.help_dialog = MDDialog(
            title=str(title),
            text=str(text),
            buttons=[
                self.create_button(
                    text=self.t("ok"),
                )
            ],
        )


        self.help_dialog.buttons[0].bind(
            on_release=lambda x:
                self.help_dialog.dismiss()
        )


        self.help_dialog.open()


    # ====================================================
    # Section title
    # ====================================================

    def add_section_title(
        self,
        parent,
        title,
        help_text,
    ):

        header = SectionHeader(
            title=title,
            help_text=help_text,

            widget_factory=self.widget_factory,

            theme=self.theme,

            on_help=self.show_help,
        )


        parent.add_widget(
            header
        )