from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu

from database.database import (
    get_configurations,
    get_spirits,
    get_boards
)

from engine.generator import generate_game
from engine.formatter import format_game

from widgets.selection_menu_item import SelectionMenuItem


class NewGameScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.players = None
        self.configuration = None

        root = MDBoxLayout(
            orientation="vertical"
        )

        self.add_top_bar(
            root,
            "Game Generator"
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

        content.add_widget(
            MDLabel(
                text="Board Configuration",
                font_style="H6"
            )
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

        content.add_widget(
            MDLabel(
                text="Players",
                font_style="H6"
            )
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

        for i in range(self.players):

            card = MDCard(
                orientation="vertical",
                padding="10dp",
                spacing="10dp",
                adaptive_height=True,
                radius=[16]
            )

            card.add_widget(
                MDLabel(
                    text=f"Player {i + 1}",
                    font_style="H6"
                )
            )

            row = MDBoxLayout(
                orientation="horizontal",
                spacing=dp(10),
                adaptive_height=True
            )

            spirit_button = MDRaisedButton(
                text="Spirit: Any",
                size_hint_x=.75
            )

            board_button = MDRaisedButton(
                text="Board: Any",
                size_hint_x=.25
            )

            spirit_button.bind(
                on_release=lambda x, idx=i: self.open_spirit_menu(idx)
            )

            board_button.bind(
                on_release=lambda x, idx=i: self.open_board_menu(idx)
            )

            row.add_widget(spirit_button)
            row.add_widget(board_button)

            card.add_widget(row)

            self.players_container.add_widget(card)

            self.player_rows.append({
                "spirit": None,
                "board": None,
                "spirit_button": spirit_button,
                "board_button": board_button
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
    
        # Remove this spirit from another player
        if spirit is not None:

            for i, row in enumerate(self.player_rows):

                if i != index and row["spirit"] == spirit:

                    row["spirit"] = None

                    row["spirit_button"].text = "Spirit: Any"


        self.player_rows[index]["spirit"] = spirit

        button = self.player_rows[index]["spirit_button"]

        button.text = (
            "Spirit: Any"
            if spirit is None
            else spirit.name
        )

        self.spirit_menu.dismiss()



    def set_board(self, index, board):
        # Remove this board from another player
        if board is not None:

            for i, row in enumerate(self.player_rows):

                if i != index and row["board"] == board:

                    row["board"] = None

                    row["board_button"].text = "Board: Any"


        self.player_rows[index]["board"] = board

        button = self.player_rows[index]["board_button"]

        button.text = (
            "Board: Any"
            if board is None
            else board.name
        )

        self.board_menu.dismiss()

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


        game = generate_game(
            players=self.players,
            configuration=self.configuration,
            spirits=spirits,
            boards=boards
        )

        self.result.text = format_game(game)