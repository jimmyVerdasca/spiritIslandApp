from kivy.uix.screenmanager import Screen

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class HomeScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            padding="20dp"
        )

        title = MDLabel(
            text="Spirit Island Companion",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height="60dp"
        )

        layout.add_widget(title)

        menu = [
            ("Current Games", "current"),
            ("New Challenge", "new"),
            ("Trophies", "trophies"),
            ("History", "history")
        ]

        for text, screen in menu:

            card = MDCard(
                size_hint_y=None,
                height="70dp",
                padding="10dp",
                radius=[20]
            )

            button = MDRaisedButton(
                text=text,
                size_hint=(1, None),
                height="50dp"
            )

            button.bind(
                on_release=lambda instance, s=screen:
                self.change_screen(s)
            )

            card.add_widget(button)

            layout.add_widget(card)

        self.add_widget(layout)


    def change_screen(self, screen):
        print("Switching to", screen)
        self.manager.current = screen