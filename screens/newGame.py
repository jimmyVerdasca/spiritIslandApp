from .baseScreen import BaseScreen

from kivy.metrics import dp

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
    get_scenarios
)

from engine.generator import generate_game
from engine.formatter import format_game

from widgets.selection_menu_item import SelectionMenuItem


class NewGameScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.players = None
        self.configuration = None
        self.adversary_rows = []
        self.scenario_rows = []

        root = MDBoxLayout(
            orientation="vertical"
        )

        self.add_top_bar(
            root,
            "Create new Game"
        )

        scroll = MDScrollView()

        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20),
            adaptive_height=True
        )

        # ----------------------------
        # Configuration
        # ----------------------------

        self.add_section_title(
            content,
            "Board Configuration",
            "The board configuration determines the island layout and "
            "the number of players supported. Leave it as Any to let "
            "the generator choose a valid configuration automatically."
        )

        self.configuration_button = MDRaisedButton(
            text="Any"
        )

        self.configuration_button.bind(
            on_release=self.open_configuration_menu
        )

        content.add_widget(
            self.configuration_button
        )

        # ----------------------------
        # Players
        # ----------------------------

        self.add_section_title(
            content,
            "Players",
            "Select the number of players for the game. If left as Any, "
            "the generator will randomly choose a valid player count "
            "based on the selected board configuration."
        )

        self.players_button = MDRaisedButton(
            text="Any"
        )

        self.players_button.bind(
            on_release=self.open_players_menu
        )

        content.add_widget(
            self.players_button
        )

        # ----------------------------
        # Per-player selection
        # ----------------------------

        self.player_rows = []

        self.players_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            adaptive_height=True
        )

        content.add_widget(
            self.players_container
        )
        
        # ----------------------------
        # adversary selection
        # ----------------------------

        self.add_section_title(
            content,
            "Adversaries",
            "Adversaries increase the challenge of the game. You can select "
            "specific adversaries and difficulty levels, or leave them as Any "
            "to allow the generator to choose randomly it will try to get a maximum total difficulty of 6 if possible."
        )

        self.add_adversary_button = MDRaisedButton(
            text="+ Add Adversary",
        )

        self.add_adversary_button.bind(
            on_release=self.add_adversary_row
        )

        content.add_widget(self.add_adversary_button)

        self.adversaries_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True,
        )

        content.add_widget(self.adversaries_container)

        row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            adaptive_height=True,
        )

        adversary_button = MDRaisedButton(
            text="Adversary: None",
            size_hint_x=.65,
        )

        level_button = MDRaisedButton(
            text="Difficulty: Any",
            size_hint_x=.25,
        )

        remove_button = MDIconButton(
            icon="close",
            size_hint_x=.1,
        )

        # ----------------------------
        # Scenario selection
        # ----------------------------

        self.add_section_title(
            content,
            "Scenarios",
            "Scenarios modify the game setup. "
            "You can select specific scenarios or leave it as Any "
            "to let the generator choose randomly."
        )


        self.add_scenario_button = MDRaisedButton(
            text="+ Add Scenario",
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

        # ----------------------------
        # Generate
        # ----------------------------

        generate = MDRaisedButton(
            text="Generate",
            pos_hint={
                "center_x": .5
            }
        )

        generate.bind(
            on_release=self.generate
        )

        content.add_widget(
            generate
        )

        # ----------------------------
        # Result
        # ----------------------------

        card = MDCard(
            orientation="vertical",
            padding="20dp",
            adaptive_height=True,
            radius=[20]
        )

        self.result = MDLabel(
            text="Press Generate",
            adaptive_height=True
        )

        card.add_widget(
            self.result
        )

        content.add_widget(
            card
        )

        scroll.add_widget(
            content
        )

        root.add_widget(
            scroll
        )

        self.add_widget(
            root
        )

    # ----------------------------------------------------
    # Menus
    # ----------------------------------------------------

    def open_players_menu(self, instance):
    
        if (
            self.configuration is not None
            and self.configuration.min_players == self.configuration.max_players
        ):
            return
        
        items = [
            {
                "text": "Any",
                "on_release": lambda: self.set_players(None)
            }
        ]

        if self.configuration is None:
            minimum = 2
            maximum = 6
        else:
            minimum = self.configuration.min_players
            maximum = self.configuration.max_players

        for i in range(minimum, maximum + 1):
            items.append(
                {
                    "text": str(i),
                    "on_release": lambda x=i: self.set_players(x)
                }
            )

        self.players_menu = MDDropdownMenu(
            caller=self.players_button,
            items=items
        )

        self.players_menu.open()

    def add_adversary_row(self, *args):
        row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            adaptive_height=True,
        )

        adversary_button = MDRaisedButton(
            text="Adversary: None",
            size_hint_x=.6,
        )

        level_button = MDRaisedButton(
            text="Difficulty: Any",
            size_hint_x=.25,
        )

        remove_button = MDIconButton(
            icon="close",
            size_hint_x=.15,
        )

        index = len(self.adversary_rows)

        adversary_button.bind(
            on_release=lambda x, i=index: self.open_adversary_menu(i)
        )

        level_button.bind(
            on_release=lambda x, i=index: self.open_level_menu(i)
        )

        row.add_widget(adversary_button)
        row.add_widget(level_button)
        row.add_widget(remove_button)

        self.adversaries_container.add_widget(row)

        self.adversary_rows.append({
            "row": row,
            "adversary": None,
            "level": None,
            "adversary_button": adversary_button,
            "level_button": level_button,
            "remove_button": remove_button,
        })


        remove_button.bind(
            on_release=lambda x, r=row:
                self.remove_adversary_row(
                    next(
                        i
                        for i, item in enumerate(self.adversary_rows)
                        if item["row"] == r
                    )
                )
        )

        self.update_adversary_button_state()

    def open_adversary_menu(self, index):
    
        adversaries = get_adversaries()

        selected = [
            row["adversary"]
            for i, row in enumerate(self.adversary_rows)
            if i != index and row["adversary"] is not None
        ]

        items = [
            {
                "text": "Any",
                "item_state": "normal",
                "viewclass": "SelectionMenuItem",
                "on_release": lambda: self.set_adversary(index, None),
            }
        ]


        for adversary in adversaries:

            # Remove already selected adversaries
            if adversary in selected:
                continue


            state = (
                "selected"
                if self.adversary_rows[index]["adversary"] == adversary
                else "normal"
            )


            items.append(
                {
                    "text": adversary.name,
                    "item_state": state,
                    "viewclass": "SelectionMenuItem",
                    "on_release": lambda a=adversary:
                        self.set_adversary(index, a),
                }
            )


        self.adversary_menu = MDDropdownMenu(
            caller=self.adversary_rows[index]["adversary_button"],
            items=items,
        )

        self.adversary_menu.open()

    def set_adversary(self, index, adversary):
    
        self.adversary_rows[index]["adversary"] = adversary

        self.adversary_rows[index]["adversary_button"].text = (
            "Adversary: Any"
            if adversary is None
            else adversary.name
        )

        self.adversary_menu.dismiss()

    def open_level_menu(self, index):
        
        difficulties = get_difficulties()

        items = [
            {
                "text": "Any",
                "item_state": "normal",
                "viewclass": "SelectionMenuItem",
                "on_release": lambda: self.set_level(index, None),
            }
        ]

        current = self.adversary_rows[index]["level"]

        for difficulty in difficulties:

            state = (
                "selected"
                if current is not None and current.id == difficulty.id
                else "normal"
            )

            items.append(
                {
                    "text": str(difficulty.level),
                    "item_state": state,
                    "viewclass": "SelectionMenuItem",
                    "on_release": lambda d=difficulty: self.set_level(index, d),
                }
            )

        self.level_menu = MDDropdownMenu(
            caller=self.adversary_rows[index]["level_button"],
            items=items,
        )

        self.level_menu.open()

    def set_level(self, index, difficulty):
    
        self.adversary_rows[index]["level"] = difficulty

        self.adversary_rows[index]["level_button"].text = (
            "Difficulty: Any"
            if difficulty is None
            else str(difficulty.level)
        )

        self.level_menu.dismiss()

    def remove_adversary_row(self, index):
    
        if index >= len(self.adversary_rows):
            return

        row = self.adversary_rows.pop(index)

        self.adversaries_container.remove_widget(row["row"])

        # Rebind buttons because indices have changed
        for i, row in enumerate(self.adversary_rows):

            row["adversary_button"].unbind(on_release=None)
            row["level_button"].unbind(on_release=None)

            row["adversary_button"].bind(
                on_release=lambda x, idx=i: self.open_adversary_menu(idx)
            )

            row["level_button"].bind(
                on_release=lambda x, idx=i: self.open_level_menu(idx)
            )
        self.update_adversary_button_state()

    def set_scenario(self,index,scenario):
    
        self.scenario_rows[index]["scenario"] = scenario


        self.scenario_rows[index]["scenario_button"].text = (
            "Scenario: Any"
            if scenario is None
            else scenario.name
        )


        self.scenario_menu.dismiss()

    def remove_scenario_row(self,index):
    
        if index >= len(self.scenario_rows):
            return


        row = self.scenario_rows.pop(index)


        self.scenarios_container.remove_widget(
            row["row"]
        )


        for i,row in enumerate(self.scenario_rows):

            row["scenario_button"].unbind(
                on_release=None
            )

            row["scenario_button"].bind(
                on_release=lambda x,idx=i:
                    self.open_scenario_menu(idx)
            )


        self.update_scenario_button_state()

    def update_scenario_button_state(self):
    
        max_scenarios = len(get_scenarios())

        self.add_scenario_button.disabled = (
            len(self.scenario_rows)
            >= max_scenarios
        )

    def open_scenario_menu(self, index):
    
        scenarios = get_scenarios()


        items = [
            {
                "text": "Any",
                "viewclass": "SelectionMenuItem",
                "on_release":
                    lambda:
                    self.set_scenario(index, None)
            }
        ]


        selected = [
            row["scenario"]
            for i,row in enumerate(self.scenario_rows)
            if i != index
            and row["scenario"] is not None
        ]


        for scenario in scenarios:

            if scenario in selected:
                continue


            state = (
                "selected"
                if self.scenario_rows[index]["scenario"] == scenario
                else "normal"
            )


            items.append(
                {
                    "text": scenario.name,
                    "item_state": state,
                    "viewclass": "SelectionMenuItem",
                    "on_release":
                        lambda s=scenario:
                        self.set_scenario(index,s)
                }
            )


        self.scenario_menu = MDDropdownMenu(
            caller=
            self.scenario_rows[index]["scenario_button"],
            items=items
        )


        self.scenario_menu.open()

    def add_scenario_row(self, *args):
    
        row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            adaptive_height=True,
        )


        scenario_button = MDRaisedButton(
            text="Scenario: Any",
            size_hint_x=.85,
        )


        remove_button = MDIconButton(
            icon="close",
            size_hint_x=.15,
        )


        index = len(self.scenario_rows)


        scenario_button.bind(
            on_release=lambda x, i=index:
                self.open_scenario_menu(i)
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
                "scenario_button": scenario_button,
                "remove_button": remove_button,
            }
        )


        remove_button.bind(
            on_release=lambda x, r=row:
                self.remove_scenario_row(
                    next(
                        i
                        for i,item in enumerate(self.scenario_rows)
                        if item["row"] == r
                    )
                )
        )


        self.update_scenario_button_state()

    def set_players(self, value):
    
        self.players = value

        self.players_button.text = (
            "Any"
            if value is None
            else str(value)
        )

        self.refresh_player_rows()

        self.players_menu.dismiss()

    def open_configuration_menu(self, instance):

        configurations = get_configurations()

        items = [
            {
                "text": "Any",
                "on_release": lambda: self.set_configuration(None)
            }
        ]

        for configuration in configurations:

            items.append(
                {
                    "text": configuration.name,
                    "on_release": lambda c=configuration: self.set_configuration(c)
                }
            )

        self.configuration_menu = MDDropdownMenu(
            caller=self.configuration_button,
            items=items
        )

        self.configuration_menu.open()

    def set_configuration(self, configuration):
    
        self.configuration = configuration

        self.configuration_button.text = (
            "Any"
            if configuration is None
            else configuration.name
        )

        if configuration is None:
            self.players = None
            self.players_button.text = "Any"

        elif configuration.min_players == configuration.max_players:
            # Only one possible player count
            self.players = configuration.min_players
            self.players_button.text = str(configuration.min_players)

        elif (
            self.players is not None
            and not (
                configuration.min_players
                <= self.players
                <= configuration.max_players
            )
        ):
            # Previous selection is no longer valid
            self.players = None
            self.players_button.text = "Any"

        self.refresh_player_rows()
        self.configuration_menu.dismiss()

    def refresh_player_rows(self):

        self.players_container.clear_widgets()
        self.player_rows = []

        if self.players is None:
            return

        # Normal spirit artwork ratio: 198 x 128
        image_ratio = 198 / 128

        for i in range(self.players):

            # ------------------------------------------------
            # Player card
            # ------------------------------------------------

            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                padding=0,
                radius=[16],
                elevation=2,
            )

            def update_card_height(card, width, ratio=image_ratio):
                if width > 0:
                    card.height = width / ratio

            card.bind(
                width=update_card_height
            )

            # ------------------------------------------------
            # Background artwork
            # ------------------------------------------------

            background = FloatLayout(
                size_hint=(1, 1),
            )

            spirit_image = Image(
                source="assets/spirits/Any.png",
                size_hint=(1, 1),
                pos_hint={"x": 0, "y": 0},
                fit_mode="cover",
            )

            background.add_widget(
                spirit_image
            )

            # ------------------------------------------------
            # Board artwork - top right corner
            # ------------------------------------------------

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

            # Dark overlay behind board name
            board_title_overlay = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, 0.35),
                pos_hint={
                    "x": 0,
                    "center_y": 0,
                },
            )

            board_name_label = MDLabel(
                text="Any",
                halign="center",
                valign="middle",

                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                opacity=1,

                font_style="H6",
            )

            board_name_label.bind(
                size=lambda instance, value:
                    setattr(instance, "text_size", value)
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

            # ------------------------------------------------
            # Dark overlay
            # ------------------------------------------------

            overlay = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, 1),
                pos_hint={"x": 0, "y": 0},
                padding=dp(10),
                spacing=dp(4),
            )

            # ------------------------------------------------
            # Player title
            # ------------------------------------------------

            player_title = MDLabel(
                text=f"Player {i + 1}",
                size_hint_y=None,
                height=dp(30),

                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),

                font_style="H5",
            )

            overlay.add_widget(
                player_title
            )

            # ------------------------------------------------
            # Spirit name
            # ------------------------------------------------

            spirit_name_label = MDLabel(
                text="",
                size_hint_y=None,
                height=dp(30),

                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),

                font_style="H6",

                # Allow long spirit names to wrap
                halign="left",
                valign="middle",
            )

            spirit_name_label.bind(
                width=lambda instance, value:
                    setattr(instance, "text_size", (value, None))
            )

            overlay.add_widget(
                spirit_name_label
            )

            # ------------------------------------------------
            # Spacer
            # ------------------------------------------------

            overlay.add_widget(
                MDBoxLayout()
            )

            # ------------------------------------------------
            # Buttons
            # ------------------------------------------------

            button_row = MDBoxLayout(
                orientation="horizontal",

                size_hint_x=1,
                size_hint_y=None,
                height=dp(45),

                spacing=dp(8),
            )

            spirit_button = MDRaisedButton(
                text="Choose Spirit",
                size_hint_x=0.55,
            )

            board_button = MDRaisedButton(
                text="Choose Board",
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

            # ------------------------------------------------
            # Assemble
            # ------------------------------------------------

            background.add_widget(
                overlay
            )

            card.add_widget(
                background
            )

            self.players_container.add_widget(
                card
            )

            # ------------------------------------------------
            # Store state
            # ------------------------------------------------

            self.player_rows.append({
                "spirit": None,
                "board": None,

                "spirit_button": spirit_button,
                "board_button": board_button,

                "spirit_name_label": spirit_name_label,
                "board_name_label": board_name_label,

                "spirit_image": spirit_image,
                "board_image": board_image,
            })




    def open_spirit_menu(self, index):
    
        spirits = get_spirits()

        items = []

        items.append(
            {
                "text": "Any",
                "item_state": "normal",
                "viewclass": "SelectionMenuItem",
                "on_release": lambda:
                    self.set_spirit(index, None)
            }
        )


        for spirit in spirits:

            state = "normal"
            label = spirit.name

            for i, row in enumerate(self.player_rows):

                if (
                    i != index
                    and row["spirit"] is not None
                    and row["spirit"].id == spirit.id
                ):
                    state = "warning"
                    label = (
                        f"{spirit.name} "
                        f"(Player {i + 1})"
                    )


                if (
                    i == index
                    and row["spirit"] is not None
                    and row["spirit"].id == spirit.id
                ):
                    state = "selected"
                    label = (
                        f"{spirit.name}"
                    )


            items.append(
                {
                    "text": label,
                    "item_state": state,
                    "viewclass": "SelectionMenuItem",
                    "on_release": lambda s=spirit:
                        self.set_spirit(index, s)
                }
            )



        self.spirit_menu = MDDropdownMenu(
            caller=self.player_rows[index]["spirit_button"],
        )

        self.spirit_menu.items = items

        self.spirit_menu.open()



    def open_board_menu(self, index):
    
        boards = get_boards()

        items = [
            {
                "text": "Any",
                "item_state": "normal",
                "viewclass": "SelectionMenuItem",
                "on_release": lambda:
                    self.set_board(index, None)
            }
        ]


        for board in boards:

            state = "normal"
            label = board.name


            for i, row in enumerate(self.player_rows):

                if (
                    i != index
                    and row["board"] is not None
                    and row["board"].id == board.id
                ):
                    state = "warning"
                    label = (
                        f"⚠ {board.name} "
                        f"(Player {i + 1})"
                    )


                if (
                    i == index
                    and row["board"] is not None
                    and row["board"].id == board.id
                ):
                    state = "selected"
                    label = (
                        f"✓ {board.name}"
                    )


            items.append(
                {
                    "text": label,
                    "item_state": state,
                    "viewclass": "SelectionMenuItem",
                    "on_release": lambda s=board:
                        self.set_board(index, s)
                }
            )


        self.board_menu = MDDropdownMenu(
            caller=self.player_rows[index]["board_button"],
        )

        self.board_menu.items = items

        self.board_menu.open()

    def set_spirit(self, index, spirit):

        print("SELECTED SPIRIT:", index, spirit)

        # ------------------------------------------------
        # Remove this spirit from another player
        # ------------------------------------------------

        if spirit is not None:

            for i, row in enumerate(self.player_rows):

                if (
                    i != index
                    and row["spirit"] == spirit
                ):

                    row["spirit"] = None

                    # Reset their labels
                    row["spirit_name_label"].text = "Choose Spirit"

                    # Reset their button
                    row["spirit_button"].text = "Choose Spirit"

                    # Reset their artwork
                    row["spirit_image"].source = (
                        "assets/spirits/Any.png"
                    )

        # ------------------------------------------------
        # Update current player
        # ------------------------------------------------

        row = self.player_rows[index]

        row["spirit"] = spirit

        if spirit is None:

            row["spirit_name_label"].text = ""
            row["spirit_button"].text = "Choose Spirit"

            row["spirit_image"].source = (
                "assets/spirits/Any.png"
            )

        else:

            # Show the full spirit name in the card
            row["spirit_name_label"].text = spirit.name

            # Button always remains the same
            row["spirit_button"].text = "Choose Spirit"

            # Show spirit artwork
            row["spirit_image"].source = (
                f"assets/spirits/{spirit.name}.png"
            )

        # ------------------------------------------------
        # Close menu
        # ------------------------------------------------

        self.spirit_menu.dismiss()



    def set_board(self, index, board):
    
        # ------------------------------------------------
        # Remove this board from another player
        # ------------------------------------------------

        if board is not None:

            for i, row in enumerate(self.player_rows):

                if (
                    i != index
                    and row["board"] == board
                ):

                    row["board"] = None

                    row["board_name_label"].text = "Any"

                    row["board_button"].text = "Choose Board"

                    row["board_image"].source = (
                        "assets/boards/Any.png"
                    )

        # ------------------------------------------------
        # Update current player
        # ------------------------------------------------

        row = self.player_rows[index]

        row["board"] = board

        if board is None:

            row["board_name_label"].text = "Any"

            row["board_button"].text = "Choose Board"

            row["board_image"].source = (
                "assets/boards/Any.png"
            )

        else:

            row["board_name_label"].text = board.name

            row["board_button"].text = "Choose Board"

            row["board_image"].source = (
                f"assets/boards/{board.name}.png"
            )

        self.board_menu.dismiss()


    def update_adversary_button_state(self):
    
        max_adversaries = len(get_adversaries())

        self.add_adversary_button.disabled = (
            len(self.adversary_rows) >= max_adversaries
        )

    # ----------------------------------------------------
    # Generate
    # ----------------------------------------------------

    def generate(self, instance):
    
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
                row["level"]
            )
            for row in self.adversary_rows
        ]

        scenarios = None

        if len(self.scenario_rows) > 0:

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

        self.result.text = format_game(game)

    def show_help(self, title, text):
    
        self.help_dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.help_dialog.dismiss()
                )
            ]
        )

        self.help_dialog.open()

    def add_section_title(self, parent, title, help_text):

        row = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            spacing=dp(5),
            size_hint_x=None,
            width=dp(250),
        )

        label = MDLabel(
            text=title,
            font_style="H5",
            size_hint_x=None,
            width=dp(180),
        )

        info = MDIconButton(
            icon="information-outline",
            size_hint_x=None,
            width=dp(40),
        )

        info.bind(
            on_release=lambda x:
                self.show_help(
                    title,
                    help_text
                )
        )

        row.add_widget(label)
        row.add_widget(info)

        parent.add_widget(row)