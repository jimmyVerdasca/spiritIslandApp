from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from database.database import (
    get_configurations,
    get_spirits,
    get_boards,
    get_adversaries,
    get_difficulties,
    get_scenarios,
)

from engine.generator import generate_game
from engine.formatter import format_game

from widgets.selection_menu_item import SelectionMenuItem


class NewGameScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # =================================================
        # Managers
        # =================================================

        app = MDApp.get_running_app()

        self.settings_manager = app.settings_manager
        self.language_manager = app.language_manager
        self.theme_manager = app.theme_manager

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
            spacing=dp(20),
            padding=dp(20),
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

        self.configuration_button = MDRaisedButton(
            text=self.t("any"),
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

        self.players_button = MDRaisedButton(
            text=self.t("any"),
        )

        self.players_button.bind(
            on_release=self.open_players_menu
        )

        content.add_widget(
            self.players_button
        )

        # =================================================
        # Per-player selection
        # =================================================

        self.players_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
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

        self.add_adversary_button = MDRaisedButton(
            text=self.t("add_adversary"),
        )

        self.add_adversary_button.bind(
            on_release=self.add_adversary_row
        )

        content.add_widget(
            self.add_adversary_button
        )

        self.adversaries_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
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

        self.add_scenario_button = MDRaisedButton(
            text=self.t("add_scenario"),
        )

        self.add_scenario_button.bind(
            on_release=self.add_scenario_row
        )

        content.add_widget(
            self.add_scenario_button
        )

        self.scenarios_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True,
        )

        content.add_widget(
            self.scenarios_container
        )

        # =================================================
        # Generate button
        # =================================================

        self.generate_button = MDRaisedButton(
            text=self.t("generate"),
            pos_hint={
                "center_x": 0.5,
            },
        )

        self.generate_button.bind(
            on_release=self.generate
        )

        content.add_widget(
            self.generate_button
        )

        # =================================================
        # Result card
        # =================================================

        self.result_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            adaptive_height=True,
            radius=[dp(20)],
        )

        self.result = MDLabel(
            text=self.t("press_generate"),
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
        self.update_theme()

    # ====================================================
    # Translation helper
    # ====================================================

    def t(self, key, *categories):

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

        # The translation file currently defines
        # "adversaries" twice:
        #
        # "adversaries": "Adversaries"
        #
        # and later:
        #
        # "adversaries": {
        #     ...
        # }
        #
        # Python keeps the second value.
        #
        # Until the translation key is renamed, use
        # the appropriate section title here.

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
        self.update_theme()

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

        # ---------------------------------------------
        # Main buttons
        # ---------------------------------------------

        if self.configuration is None:

            self.configuration_button.text = self.t(
                "any"
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

        self.add_adversary_button.text = self.t(
            "add_adversary"
        )

        self.add_scenario_button.text = self.t(
            "add_scenario"
        )

        self.generate_button.text = self.t(
            "generate"
        )

        # ---------------------------------------------
        # Existing adversary rows
        # ---------------------------------------------

        for row in self.adversary_rows:

            adversary = row["adversary"]
            level = row["level"]

            if adversary is None:

                row["adversary_button"].text = (
                    f"{self.t('adversaries_title')}: "
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

        # ---------------------------------------------
        # Existing scenario rows
        # ---------------------------------------------

        for row in self.scenario_rows:

            scenario = row["scenario"]

            row["scenario_button"].text = (

                f"{self.t('scenario')}: "
                f"{self.t('any')}"
                if scenario is None
                else (
                    f"{self.t('scenario')}: "
                    f"{self.scenario_name(scenario)}"
                )
            )

        # ---------------------------------------------
        # Existing player rows
        # ---------------------------------------------

        for index, row in enumerate(
            self.player_rows
        ):

            row["spirit_button"].text = self.t(
                "choose_spirit"
            )

            row["board_button"].text = self.t(
                "choose_board"
            )

            row["spirit_name_label"].text = (

                ""
                if row["spirit"] is None
                else self.spirit_name(
                    row["spirit"]
                )
            )

            row["board_name_label"].text = (

                self.t("any")
                if row["board"] is None
                else self.board_name(
                    row["board"]
                )
            )

            if "player_title" in row:

                row["player_title"].text = (
                    f"{self.t('player')} "
                    f"{index + 1}"
                )

        # ---------------------------------------------
        # Result
        # ---------------------------------------------

        if not self.result.text:

            self.result.text = self.t(
                "press_generate"
            )

    # ====================================================
    # Data translation helpers
    # ====================================================

    def spirit_name(self, spirit):

        return self.t(
            self.spirit_key(spirit),
            "spirits",
        )

    def adversary_name(self, adversary):

        return self.t(
            self.adversary_key(adversary),
            "adversaries",
        )

    def scenario_name(self, scenario):

        return self.t(
            self.scenario_key(scenario),
            "scenarios",
        )

    def board_name(self, board):

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
    def normalize_key(value):

        return (
            str(value)
            .strip()
            .lower()
            .replace("'", "")
            .replace("-", "_")
            .replace(" ", "_")
        )

    def spirit_key(self, spirit):

        if hasattr(spirit, "key"):
            return spirit.key

        if hasattr(spirit, "slug"):
            return spirit.slug

        if hasattr(spirit, "name"):
            return self.normalize_key(
                spirit.name
            )

        return str(spirit)

    def adversary_key(self, adversary):

        if hasattr(adversary, "key"):
            return adversary.key

        if hasattr(adversary, "slug"):
            return adversary.slug

        if hasattr(adversary, "name"):
            return self.normalize_key(
                adversary.name
            )

        return str(adversary)

    def scenario_key(self, scenario):

        if hasattr(scenario, "key"):
            return scenario.key

        if hasattr(scenario, "slug"):
            return scenario.slug

        if hasattr(scenario, "name"):
            return self.normalize_key(
                scenario.name
            )

        return str(scenario)

    def board_key(self, board):

        if hasattr(board, "key"):
            return board.key

        if hasattr(board, "slug"):
            return board.slug

        if hasattr(board, "name"):
            return self.normalize_key(
                board.name
            )

        return str(board)

    def configuration_key(
        self,
        configuration,
    ):

        if hasattr(configuration, "key"):
            return configuration.key

        if hasattr(configuration, "slug"):
            return configuration.slug

        if hasattr(configuration, "name"):
            return self.normalize_key(
                configuration.name
            )

        return str(configuration)

    # ====================================================
    # Theme
    # ====================================================

    def update_theme(self):

        self.result_card.md_bg_color = (
            self.theme_manager.get(
                "card"
            )
        )

        self.apply_label_theme(
            self.result,
            "card_text_secondary",
        )

        for row in self.player_rows:

            if "player_title" in row:

                self.apply_label_theme(
                    row["player_title"],
                    "text_primary",
                )

            self.apply_label_theme(
                row["spirit_name_label"],
                "text_primary",
            )

            self.apply_label_theme(
                row["board_name_label"],
                "text_primary",
            )

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

        configurations = get_configurations()

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
            else self.configuration_name(
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

        row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            adaptive_height=True,
        )

        adversary_button = MDRaisedButton(
            text=(
                f"{self.adversaries_title()}: "
                f"{self.t('any')}"
            ),
            size_hint_x=0.6,
        )

        level_button = MDRaisedButton(
            text=(
                f"{self.t('difficulty')}: "
                f"{self.t('any')}"
            ),
            size_hint_x=0.25,
        )

        remove_button = MDIconButton(
            icon="close",
            size_hint_x=0.15,
        )

        row.add_widget(
            adversary_button
        )

        row.add_widget(
            level_button
        )

        row.add_widget(
            remove_button
        )

        self.adversaries_container.add_widget(
            row
        )

        self.adversary_rows.append(
            {
                "row": row,
                "adversary": None,
                "level": None,
                "adversary_button":
                    adversary_button,
                "level_button":
                    level_button,
                "remove_button":
                    remove_button,
            }
        )

        remove_button.bind(
            on_release=lambda x, r=row:
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

        adversaries = get_adversaries()

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
                else "normal"
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
            else (
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

        difficulties = get_difficulties()

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
                else "normal"
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
            else (
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

        self.update_adversary_button_state()

    # ====================================================
    # Adversary button state
    # ====================================================

    def update_adversary_button_state(
        self,
    ):

        max_adversaries = len(
            get_adversaries()
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

        row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            adaptive_height=True,
        )

        scenario_button = MDRaisedButton(
            text=(
                f"{self.t('scenario')}: "
                f"{self.t('any')}"
            ),
            size_hint_x=0.85,
        )

        remove_button = MDIconButton(
            icon="close",
            size_hint_x=0.15,
        )

        row.add_widget(
            scenario_button
        )

        row.add_widget(
            remove_button
        )

        self.scenarios_container.add_widget(
            row
        )

        self.scenario_rows.append(
            {
                "row": row,
                "scenario": None,
                "scenario_button":
                    scenario_button,
                "remove_button":
                    remove_button,
            }
        )

        scenario_button.bind(
            on_release=lambda x, r=row:
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

        remove_button.bind(
            on_release=lambda x, r=row:
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

        scenarios = get_scenarios()

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
                else "normal"
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
            else (
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
            get_scenarios()
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

        image_ratio = 198 / 128

        for i in range(
            self.players
        ):

            # -----------------------------------------
            # Player card
            # -----------------------------------------

            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                padding=0,
                radius=[dp(16)],
                elevation=2,
            )

            def update_card_height(
                card,
                width,
                ratio=image_ratio,
            ):

                if width > 0:

                    card.height = (
                        width / ratio
                    )

            card.bind(
                width=update_card_height
            )

            # -----------------------------------------
            # Background
            # -----------------------------------------

            background = FloatLayout(
                size_hint=(1, 1),
            )

            spirit_image = Image(
                source="assets/spirits/Any.png",
                size_hint=(1, 1),
                pos_hint={
                    "x": 0,
                    "y": 0,
                },
                fit_mode="cover",
            )

            background.add_widget(
                spirit_image
            )

            # -----------------------------------------
            # Board
            # -----------------------------------------

            board_container = FloatLayout(
                size_hint=(0.40, 0.40),
                pos_hint={
                    "right": 0.98,
                    "top": 0.98,
                },
            )

            board_image = Image(
                source="assets/boards/Any.png",
                size_hint=(1, 1),
                pos_hint={
                    "x": 0,
                    "y": -0.5,
                },
                fit_mode="contain",
            )

            board_container.add_widget(
                board_image
            )

            board_title_overlay = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, 0.35),
                pos_hint={
                    "x": 0,
                    "center_y": 0,
                },
            )

            board_name_label = MDLabel(
                text=self.t("any"),
                halign="center",
                valign="middle",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_style="H6",
            )

            board_name_label.bind(
                size=lambda instance, value:
                    setattr(
                        instance,
                        "text_size",
                        value,
                    )
            )

            board_title_overlay.add_widget(
                board_name_label
            )

            board_container.add_widget(
                board_title_overlay
            )

            background.add_widget(
                board_container
            )

            # -----------------------------------------
            # Overlay
            # -----------------------------------------

            overlay = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, 1),
                pos_hint={
                    "x": 0,
                    "y": 0,
                },
                padding=dp(10),
                spacing=dp(4),
            )

            # -----------------------------------------
            # Player title
            # -----------------------------------------

            player_title = MDLabel(
                text=(
                    f"{self.t('player')} "
                    f"{i + 1}"
                ),
                size_hint_y=None,
                height=dp(30),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_style="H5",
            )

            overlay.add_widget(
                player_title
            )

            # -----------------------------------------
            # Spirit name
            # -----------------------------------------

            spirit_name_label = MDLabel(
                text="",
                size_hint_y=None,
                height=dp(30),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_style="H6",
                halign="left",
                valign="middle",
            )

            spirit_name_label.bind(
                width=lambda instance, value:
                    setattr(
                        instance,
                        "text_size",
                        (value, None),
                    )
            )

            overlay.add_widget(
                spirit_name_label
            )

            # -----------------------------------------
            # Spacer
            # -----------------------------------------

            overlay.add_widget(
                MDBoxLayout()
            )

            # -----------------------------------------
            # Buttons
            # -----------------------------------------

            button_row = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=1,
                size_hint_y=None,
                height=dp(45),
                spacing=dp(8),
            )

            spirit_button = MDRaisedButton(
                text=self.t(
                    "choose_spirit"
                ),
                size_hint_x=0.55,
            )

            board_button = MDRaisedButton(
                text=self.t(
                    "choose_board"
                ),
                size_hint_x=0.45,
            )

            spirit_button.bind(
                on_release=lambda x, idx=i:
                    self.open_spirit_menu(idx)
            )

            board_button.bind(
                on_release=lambda x, idx=i:
                    self.open_board_menu(idx)
            )

            button_row.add_widget(
                spirit_button
            )

            button_row.add_widget(
                board_button
            )

            overlay.add_widget(
                button_row
            )

            # -----------------------------------------
            # Assemble
            # -----------------------------------------

            background.add_widget(
                overlay
            )

            card.add_widget(
                background
            )

            self.players_container.add_widget(
                card
            )

            # -----------------------------------------
            # Store state
            # -----------------------------------------

            self.player_rows.append(
                {
                    "spirit": None,
                    "board": None,

                    "spirit_button":
                        spirit_button,

                    "board_button":
                        board_button,

                    "spirit_name_label":
                        spirit_name_label,

                    "board_name_label":
                        board_name_label,

                    "spirit_image":
                        spirit_image,

                    "board_image":
                        board_image,

                    "player_title":
                        player_title,
                }
            )

        self.update_theme()

    # ====================================================
    # Spirit menu
    # ====================================================

    def open_spirit_menu(
        self,
        index,
    ):

        spirits = get_spirits()

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
                    and row["spirit"].id
                    == spirit.id
                ):

                    row["spirit"] = None

                    row["spirit_name_label"].text = ""

                    row["spirit_image"].source = (
                        "assets/spirits/Any.png"
                    )

        row = self.player_rows[index]

        row["spirit"] = spirit

        if spirit is None:

            row["spirit_name_label"].text = ""

            row["spirit_image"].source = (
                "assets/spirits/Any.png"
            )

        else:

            row["spirit_name_label"].text = (
                self.spirit_name(spirit)
            )

            row["spirit_image"].source = (
                f"assets/spirits/{spirit.key}.png"
            )

        if self.spirit_menu:

            self.spirit_menu.dismiss()

    # ====================================================
    # Board menu
    # ====================================================

    def open_board_menu(
        self,
        index,
    ):

        boards = get_boards()

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
                    and row["board"].id
                    == board.id
                ):

                    row["board"] = None

                    row["board_name_label"].text = (
                        self.t("any")
                    )

                    row["board_image"].source = (
                        "assets/boards/Any.png"
                    )

        row = self.player_rows[index]

        row["board"] = board

        if board is None:

            row["board_name_label"].text = (
                self.t("any")
            )

            row["board_image"].source = (
                "assets/boards/Any.png"
            )

        else:

            row["board_name_label"].text = (
                self.board_name(board)
            )

            row["board_image"].source = (
                f"assets/boards/{board.key}.png"
            )

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
            players=self.players,
            configuration=self.configuration,
            spirits=spirits,
            boards=boards,
            adversaries=adversaries,
            scenarios=scenarios,
        )

        self.result.text = format_game(
            game
        )

        self.apply_label_theme(
            self.result,
            "card_text_secondary",
        )

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
                MDRaisedButton(
                    text=self.t("ok"),
                    on_release=lambda x:
                        self.help_dialog.dismiss(),
                )
            ],
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

        row = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            spacing=dp(5),
            size_hint_x=None,
            width=dp(250),
        )

        label = MDLabel(
            text=str(title),
            font_style="H5",
            size_hint_x=None,
            width=dp(180),
        )

        self.apply_label_theme(
            label,
            "text_primary",
        )

        info = MDIconButton(
            icon="information-outline",
            size_hint_x=None,
            width=dp(40),
        )

        info.bind(
            on_release=lambda x:
                self.show_help(
                    str(title),
                    str(help_text),
                )
        )

        row.add_widget(
            label
        )

        row.add_widget(
            info
        )

        parent.add_widget(
            row
        )