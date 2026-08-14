from kivy.metrics import dp, sp


class ThemeHelper:

    """
    Provides convenient access to application design tokens.

    ThemeManager remains the single source of truth.

    Responsibilities:
        - Spacing
        - Dimensions
        - Icon sizes
        - Font sizes
        - Line heights
        - Colors
    """

    def __init__(self, theme_manager):

        self.theme_manager = theme_manager


    # ====================================================
    # Spacing
    # ====================================================

    def spacing(self, key):

        value = self.theme_manager.spacing(
            key
        )

        if value is None:
            return 0

        return dp(value)


    # ====================================================
    # Dimensions
    # ====================================================

    def dimension(self, component, key):

        value = self.theme_manager.get_component(
            component,
            key,
        )

        if value is None:
            return 0

        return dp(value)


    # ====================================================
    # Icon size
    # ====================================================

    def icon_size(self, size):

        value = self.theme_manager.icon_size(
            size
        )

        if value is None:
            return 0

        return dp(value)


    # ====================================================
    # Font size
    # ====================================================

    def font_size(self, style):

        value = self.theme_manager.font_size(
            style
        )

        if value is None:
            return 0

        return sp(value)


    # ====================================================
    # Line height
    # ====================================================

    def line_height(self, style):

        return self.theme_manager.line_height(
            style
        )


    # ====================================================
    # Theme value
    # ====================================================

    def get(self, key):

        return self.theme_manager.get(
            key
        )