from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu

from database.database import get_configurations
from engine.generator import generate_game
from engine.formatter import format_game


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

        self.configuration_menu.dismiss()

    # ----------------------------------------------------
    # Generate
    # ----------------------------------------------------

    def generate(self, instance):

        game = generate_game(
            players=self.players,
            board=(
                None
                if self.configuration is None
                else self.configuration.name
            )
        )

        self.result.text = format_game(game)