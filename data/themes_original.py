THEMES = {

    # =========================================================
    # COLOR PALETTE
    # =========================================================
    #
    # All actual RGBA values live here.
    #
    # Dark and light themes should only reference palette
    # values, for example:
    #
    #     "button": "palette.green.500"
    #
    # This makes the palette the single source of truth for
    # all colors used by the application.
    # =========================================================

    "palette": {

        # =====================================================
        # NEUTRAL
        # =====================================================

        "neutral": {

            "0":
                (1.00, 1.00, 1.00, 1),

            "50":
                (0.98, 0.98, 0.98, 1),

            "100":
                (0.95, 0.95, 0.96, 1),

            "200":
                (0.89, 0.89, 0.91, 1),

            "300":
                (0.78, 0.78, 0.81, 1),

            "400":
                (0.63, 0.63, 0.67, 1),

            "500":
                (0.48, 0.48, 0.52, 1),

            "600":
                (0.36, 0.36, 0.40, 1),

            "700":
                (0.25, 0.25, 0.29, 1),

            "800":
                (0.16, 0.16, 0.19, 1),

            "850":
                (0.11, 0.11, 0.13, 1),

            "900":
                (0.07, 0.07, 0.08, 1),

            "950":
                (0.04, 0.04, 0.05, 1),
        },


        # =====================================================
        # GREEN
        # =====================================================

        "green": {

            "100":
                (0.86, 0.95, 0.87, 1),

            "200":
                (0.70, 0.88, 0.72, 1),

            "300":
                (0.50, 0.78, 0.53, 1),

            "400":
                (0.30, 0.67, 0.35, 1),

            "500":
                (0.18, 0.56, 0.25, 1),

            "600":
                (0.13, 0.45, 0.20, 1),

            "700":
                (0.10, 0.35, 0.16, 1),

            "800":
                (0.07, 0.25, 0.12, 1),
        },


        # =====================================================
        # AMBER
        # =====================================================

        "amber": {

            "100":
                (1.00, 0.94, 0.78, 1),

            "200":
                (0.98, 0.84, 0.50, 1),

            "300":
                (0.94, 0.72, 0.25, 1),

            "400":
                (0.86, 0.58, 0.10, 1),

            "500":
                (0.75, 0.46, 0.06, 1),

            "600":
                (0.60, 0.34, 0.04, 1),
        },


        # =====================================================
        # RED
        # =====================================================

        "red": {

            "100":
                (1.00, 0.86, 0.86, 1),

            "200":
                (0.96, 0.68, 0.68, 1),

            "300":
                (0.90, 0.45, 0.45, 1),

            "400":
                (0.82, 0.24, 0.24, 1),

            "500":
                (0.70, 0.14, 0.14, 1),

            "600":
                (0.55, 0.08, 0.08, 1),
        },


        # =====================================================
        # BLUE
        # =====================================================

        "blue": {

            "100":
                (0.84, 0.92, 1.00, 1),

            "200":
                (0.65, 0.82, 0.98, 1),

            "300":
                (0.40, 0.68, 0.92, 1),

            "400":
                (0.22, 0.52, 0.80, 1),

            "500":
                (0.14, 0.40, 0.68, 1),

            "600":
                (0.08, 0.28, 0.52, 1),
        },


        # =====================================================
        # SPECIAL / OVERLAYS
        # =====================================================
        #
        # These are also palette colors because they are
        # concrete RGBA values used throughout the app.
        # =====================================================

        "overlay": {

            "black_50":
                (0.00, 0.00, 0.00, 0.50),

            "black_65":
                (0.00, 0.00, 0.00, 0.65),

            "black_78":
                (0.00, 0.00, 0.00, 0.78),

            "black_85":
                (0.00, 0.00, 0.00, 0.85),

            "white_30":
                (1.00, 1.00, 1.00, 0.30),

            "white_55":
                (1.00, 1.00, 1.00, 0.55),

            "white_65":
                (1.00, 1.00, 1.00, 0.65),

            "white_75":
                (1.00, 1.00, 1.00, 0.75),

            "white_80":
                (1.00, 1.00, 1.00, 0.80),

            "white_82":
                (1.00, 1.00, 1.00, 0.82),

            "white_85":
                (1.00, 1.00, 1.00, 0.85),

            "white_88":
                (1.00, 1.00, 1.00, 0.88),

            "transparent":
                (0.00, 0.00, 0.00, 0.00),
        },
    },


    # =========================================================
    # DARK THEME
    # =========================================================

    "dark": {

        # -----------------------------------------------------
        # Background
        # -----------------------------------------------------

        "background":
            "palette.neutral.900",

        "background_overlay":
            "palette.overlay.black_50",


        # -----------------------------------------------------
        # Top bar
        # -----------------------------------------------------

        "top_bar":
            "palette.green.500",

        "top_bar_button":
            "palette.green.500",


        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        "button":
            "palette.green.500",

        "button_disabled":
            "palette.neutral.700",

        "inactive_button":
            "palette.neutral.700",


        # -----------------------------------------------------
        # Semantic states
        # -----------------------------------------------------

        "success":
            "palette.green.500",

        "defeat":
            "palette.red.400",

        "warning":
            "palette.amber.400",

        "selection_warning":
            "palette.amber.400",


        # -----------------------------------------------------
        # Cards
        # -----------------------------------------------------

        "card":
            "palette.overlay.black_85",

        "card_pressed":
            "palette.neutral.700",

        "card_overlay":
            "palette.overlay.black_78",

        "card_text_secondary":
            "palette.overlay.white_65",


        # -----------------------------------------------------
        # Player cards
        #
        # Player card text is always white because artwork
        # is used as the background in both themes.
        # -----------------------------------------------------

        "player_card_text":
            "palette.neutral.0",


        # -----------------------------------------------------
        # Trophy states
        # -----------------------------------------------------

        "trophy_unlocked":
            "palette.green.800",

        "trophy_locked":
            "palette.neutral.700",


        # -----------------------------------------------------
        # Spirit cards
        # -----------------------------------------------------

        "spirit_card":
            "palette.neutral.900",

        "spirit_card_empty":
            "palette.neutral.800",

        "spirit_card_pressed":
            "palette.neutral.700",

        "spirit_name_background":
            "palette.overlay.black_78",

        "spirit_text":
            "palette.neutral.0",

        "spirit_empty_text":
            "palette.neutral.300",


        # -----------------------------------------------------
        # Text
        # -----------------------------------------------------

        "text_primary":
            "palette.neutral.0",

        "text_secondary":
            "palette.overlay.white_80",

        "text_muted":
            "palette.overlay.white_55",


        # -----------------------------------------------------
        # Icons
        # -----------------------------------------------------

        "icon":
            "palette.neutral.0",


        # -----------------------------------------------------
        # Progress
        # -----------------------------------------------------

        "progress":
            "palette.green.400",


        # -----------------------------------------------------
        # Selection
        # -----------------------------------------------------

        "selection_selected":
            "palette.green.500",

        "selection_normal":
            "palette.neutral.700",


        # -----------------------------------------------------
        # Dropdown
        # -----------------------------------------------------

        "dropdown_background":
            "palette.neutral.800",

        "dropdown_text":
            "palette.neutral.0",

        "dropdown_selected":
            "palette.green.800",

        "dropdown_text_selected":
            "palette.green.300",

        "dropdown_warning":
            "palette.amber.600",

        "dropdown_text_warning":
            "palette.amber.200",
    },


    # =========================================================
    # LIGHT THEME
    # =========================================================

    "light": {

        # -----------------------------------------------------
        # Background
        # -----------------------------------------------------

        "background":
            "palette.neutral.100",

        "background_overlay":
            "palette.overlay.white_30",


        # -----------------------------------------------------
        # Top bar
        # -----------------------------------------------------

        "top_bar":
            "palette.green.500",

        "top_bar_button":
            "palette.green.500",


        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        "button":
            "palette.green.500",

        "button_disabled":
            "palette.neutral.300",

        "inactive_button":
            "palette.neutral.200",


        # -----------------------------------------------------
        # Semantic states
        # -----------------------------------------------------

        "success":
            "palette.green.500",

        "defeat":
            "palette.red.400",

        "warning":
            "palette.amber.400",

        "selection_warning":
            "palette.amber.400",


        # -----------------------------------------------------
        # Cards
        # -----------------------------------------------------

        "card":
            "palette.overlay.white_88",

        "card_pressed":
            "palette.neutral.200",

        "card_overlay":
            "palette.overlay.white_85",

        "card_text_secondary":
            "palette.overlay.black_65",


        # -----------------------------------------------------
        # Player cards
        #
        # Intentionally identical to the dark theme.
        # -----------------------------------------------------

        "player_card_text":
            "palette.neutral.0",


        # -----------------------------------------------------
        # Trophy states
        # -----------------------------------------------------

        "trophy_unlocked":
            "palette.green.100",

        "trophy_locked":
            "palette.neutral.300",


        # -----------------------------------------------------
        # Spirit cards
        # -----------------------------------------------------

        "spirit_card":
            "palette.neutral.50",

        "spirit_card_empty":
            "palette.neutral.100",

        "spirit_card_pressed":
            "palette.neutral.200",

        "spirit_name_background":
            "palette.overlay.white_82",

        "spirit_text":
            "palette.neutral.900",

        "spirit_empty_text":
            "palette.neutral.600",


        # -----------------------------------------------------
        # Text
        # -----------------------------------------------------

        "text_primary":
            "palette.neutral.900",

        "text_secondary":
            "palette.overlay.black_65",

        "text_muted":
            "palette.overlay.black_50",


        # -----------------------------------------------------
        # Icons
        # -----------------------------------------------------

        "icon":
            "palette.neutral.900",


        # -----------------------------------------------------
        # Progress
        # -----------------------------------------------------

        "progress":
            "palette.green.500",


        # -----------------------------------------------------
        # Selection
        # -----------------------------------------------------

        "selection_selected":
            "palette.green.500",

        "selection_normal":
            "palette.neutral.200",


        # -----------------------------------------------------
        # Dropdown
        # -----------------------------------------------------

        "dropdown_background":
            "palette.neutral.0",

        "dropdown_text":
            "palette.neutral.900",

        "dropdown_selected":
            "palette.green.100",

        "dropdown_text_selected":
            "palette.green.700",

        "dropdown_warning":
            "palette.amber.100",

        "dropdown_text_warning":
            "palette.amber.600",
    },


    # =========================================================
    # DIMENSIONS
    # =========================================================

    "dimensions": {

        "spacing": {
            "xs": 4,
            "sm": 8,
            "md": 12,
            "lg": 16,
            "xl": 24,
            "xxl": 32,
        },

        "screen": {
            "padding": 20,
            "content_spacing": 12,
        },

        "top_bar": {
            "height": 56,
            "horizontal_padding": 16,
            "spacing": 8,
        },

        "card": {
            "height": 80,
            "padding": 16,
            "spacing": 12,
            "radius": 16,
            "border_width": 1,
        },

        "button": {
            "height": 48,
            "radius": 12,
            "horizontal_padding": 16,
        },

        "input": {
            "height": 48,
            "radius": 8,
            "horizontal_padding": 12,
        },

        "selection": {
            "height": 48,
            "radius": 12,
            "horizontal_padding": 12,
        },

        "icon": {
            "small": 18,
            "medium": 24,
            "large": 32,
        },

        "border": {
            "thin": 1,
            "medium": 2,
        },

        "progress": {
            "height": 15,
        },
    },


    # =========================================================
    # TYPOGRAPHY
    # =========================================================

    "typography": {

        "display": {
            "font_size": 34,
            "line_height": 1.20,
        },

        "title": {
            "font_size": 24,
            "line_height": 1.20,
        },

        "subtitle": {
            "font_size": 18,
            "line_height": 1.30,
        },

        "body": {
            "font_size": 16,
            "line_height": 1.40,
        },

        "secondary": {
            "font_size": 14,
            "line_height": 1.40,
        },

        "caption": {
            "font_size": 12,
            "line_height": 1.30,
        },

        "button": {
            "font_size": 14,
        },

        "input": {
            "font_size": 16,
        },

        "score": {
            "font_size": 20,
            "line_height": 1.20,
        },
    },
}