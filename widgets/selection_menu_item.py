from kivy.factory import Factory
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class SelectionMenuItem(MDCard):

    text = StringProperty("")
    item_state = StringProperty("normal")

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        app = MDApp.get_running_app()

        self.theme_manager = app.theme_manager

        self.size_hint_y = None
        self.height = "48dp"

        self.radius = [8]

        self.label = MDLabel(
            text=self.text,
            valign="middle",
            theme_text_color="Custom",
        )

        self.add_widget(
            self.label
        )

        self.bind(
            text=self.update_text,
            item_state=self.update_color,
        )

        self.update_color(
            self,
            self.item_state
        )


    # =================================================
    # Theme colors
    # =================================================

    def get_color(self, key):

        return self.theme_manager.get(key)


    # =================================================
    # Text
    # =================================================

    def update_text(self, instance, value):

        self.label.text = value


    # =================================================
    # Color
    # =================================================

    def update_color(self, instance, value):

        if value == "selected":

            background = self.get_color(
                "dropdown_selected"
            )

            text_color = self.get_color(
                "dropdown_text_selected"
            )

        elif value == "warning":

            background = self.get_color(
                "dropdown_warning"
            )

            text_color = self.get_color(
                "dropdown_text_warning"
            )

        else:

            background = self.get_color(
                "dropdown_background"
            )

            text_color = self.get_color(
                "dropdown_text"
            )

        self.md_bg_color = background

        self.label.text_color = text_color


Factory.register(
    "SelectionMenuItem",
    cls=SelectionMenuItem
)