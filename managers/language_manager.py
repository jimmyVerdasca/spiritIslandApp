from data.translations import TRANSLATIONS


class LanguageManager:

    def __init__(self, language="en"):

        self.current_language = language


    def set_language(self, language):

        self.current_language = language


    def get(self, key):

        return TRANSLATIONS[
            self.current_language
        ].get(
            key,
            key
        )