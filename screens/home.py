from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from engine.generator import generate_game
from engine.formatter import format_game


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical"
        )

        self.result = Label(
            text="Spirit Island Companion"
        )

        button = Button(
            text="Generate Game"
        )

        button.bind(
            on_press=self.generate
        )

        layout.add_widget(
            self.result
        )

        layout.add_widget(
            button
        )

        self.add_widget(
            layout
        )


    def generate(self, instance):

        game = generate_game(        )

        self.result.text = format_game(game)