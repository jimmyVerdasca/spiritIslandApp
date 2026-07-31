from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton


from engine.generator import generate_game
from engine.formatter import format_game


class NewGameScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        root = MDBoxLayout(
            orientation="vertical"
        )


        # fixed top navigation
        self.add_top_bar(
            root,
            "Game Generator"
        )


        # page content
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20)
        )


        self.result = MDLabel(
            text="Press Generate",
            halign="center",
            font_style="H5",
            valign="center"
        )


        button = MDRaisedButton(
            text="Generate",
            pos_hint={
                "center_x": 0.5
            }
        )


        button.bind(
            on_release=self.generate
        )


        content.add_widget(
            self.result
        )

        content.add_widget(
            button
        )


        root.add_widget(
            content
        )


        self.add_widget(
            root
        )


    def generate(self, instance):

        game = generate_game()

        text = format_game(game)

        print(text)

        self.result.text = text