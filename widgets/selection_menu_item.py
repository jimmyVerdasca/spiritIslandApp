from kivy.factory import Factory
from kivy.properties import StringProperty

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class SelectionMenuItem(MDCard):

    text = StringProperty("")
    item_state = StringProperty("normal")

    COLORS = {
        "normal": (1, 1, 1, 1),
        "warning": (0.8, 0.2, 0.2, 0.5),
        "selected": (0.2, 0.7, 0.2, 1),
    }

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = "48dp"

        self.radius = [8]

        self.md_bg_color = self.COLORS.get(
            self.item_state,
            self.COLORS["normal"]
        )

        self.label = MDLabel(
            text=self.text,
            valign="middle"
        )

        self.add_widget(self.label)

        self.bind(
            text=self.update_text,
            item_state=self.update_color
        )

    def update_text(self, instance, value):
        self.label.text = value

    def update_color(self, instance, value):
        self.md_bg_color = self.COLORS.get(
            value,
            self.COLORS["normal"]
        )


Factory.register(
    "SelectionMenuItem",
    cls=SelectionMenuItem
)