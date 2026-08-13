from data.themes import THEMES


class ThemeManager:

    """
    Central manager for the application's design system.

    Handles:

        - Light / dark color themes
        - Shared dimensions
        - Typography
        - Component design tokens

    Structure expected from THEMES:

        THEMES = {
            "dark": {...},
            "light": {...},

            "dimensions": {...},

            "typography": {...},
        }
    """

    DEFAULT_THEME = "dark"

    NON_COLOR_SECTIONS = {
        "dimensions",
        "typography",
    }

    def __init__(self, theme=None):

        self.current_theme = (
            theme
            if theme in self.available_themes()
            else self.DEFAULT_THEME
        )
        self._theme_listeners = []


    # ====================================================
    # Themes
    # ====================================================

    def available_themes(self):

        return [
            key
            for key, value in THEMES.items()
            if (
                isinstance(value, dict)
                and key not in self.NON_COLOR_SECTIONS
            )
        ]


    def set_theme(self, theme):
        
        if theme not in self.available_themes():

            raise ValueError(
                f"Unknown theme: {theme}"
            )

        if theme == self.current_theme:
            return

        self.current_theme = theme

        self._notify_theme_change()


    def get_theme(self):

        return self.current_theme


    # ====================================================
    # Colors
    # ====================================================

    def get(self, key, default=None):

        """
        Get a color from the active theme.

        Example:

            theme_manager.get("background")
            theme_manager.get("card")
            theme_manager.get("text_primary")
        """

        theme = THEMES.get(
            self.current_theme,
            {}
        )

        return theme.get(
            key,
            default
        )


    # ====================================================
    # Dimensions
    # ====================================================

    def get_dimensions(
        self,
        section=None,
        key=None,
        default=None,
    ):

        """
        Access shared dimension tokens.

        Examples:

            get_dimensions()

            get_dimensions("screen")

            get_dimensions(
                "screen",
                "padding"
            )

            get_dimensions(
                "card",
                "radius"
            )
        """

        dimensions = THEMES.get(
            "dimensions",
            {}
        )

        if section is None:

            return dimensions


        section_data = dimensions.get(
            section
        )

        if section_data is None:

            return default


        if key is None:

            return section_data


        return section_data.get(
            key,
            default
        )


    # ====================================================
    # Typography
    # ====================================================

    def get_typography(
        self,
        style=None,
        key=None,
        default=None,
    ):

        """
        Access typography tokens.

        Examples:

            get_typography()

            get_typography("title")

            get_typography(
                "title",
                "font_size"
            )
        """

        typography = THEMES.get(
            "typography",
            {}
        )

        if style is None:

            return typography


        style_data = typography.get(
            style
        )

        if style_data is None:

            return default


        if key is None:

            return style_data


        return style_data.get(
            key,
            default
        )


    # ====================================================
    # Component tokens
    # ====================================================

    def get_component(
        self,
        component,
        key=None,
        default=None,
    ):

        return self.get_dimensions(
            component,
            key,
            default,
        )


    # ====================================================
    # Spacing
    # ====================================================

    def spacing(
        self,
        size,
        default=None,
    ):

        return self.get_dimensions(
            "spacing",
            size,
            default,
        )


    # ====================================================
    # Icon sizes
    # ====================================================

    def icon_size(
        self,
        size,
        default=None,
    ):

        return self.get_dimensions(
            "icon",
            size,
            default,
        )


    # ====================================================
    # Typography helpers
    # ====================================================

    def font_size(
        self,
        style,
        default=None,
    ):

        return self.get_typography(
            style,
            "font_size",
            default,
        )


    def line_height(
        self,
        style,
        default=None,
    ):

        return self.get_typography(
            style,
            "line_height",
            default,
        )

    # ====================================================
    # Theme listeners
    # ====================================================

    def bind_theme_change(
        self,
        callback
    ):

        if callback not in self._theme_listeners:

            self._theme_listeners.append(
                callback
            )


    def unbind_theme_change(
        self,
        callback
    ):

        if callback in self._theme_listeners:

            self._theme_listeners.remove(
                callback
            )


    def _notify_theme_change(self):

        for callback in self._theme_listeners[:]:

            callback(
                self.current_theme
            )