from data.themes import THEMES


class ThemeManager:

    def __init__(self, theme="dark"):

        self.current_theme = theme


    def set_theme(self, theme):

        self.current_theme = theme


    def get(self, key):

        return THEMES[
            self.current_theme
        ].get(
            key
        )