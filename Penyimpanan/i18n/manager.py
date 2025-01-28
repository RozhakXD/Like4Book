import json
import os

class I18nManager:
    def __init__(self):
        self.current_lang = 'id'  # Default language
        self.translations = {}
        self._load_translations()
    
    def _load_translations(self):
        """Load all available language files"""
        i18n_dir = os.path.dirname(os.path.abspath(__file__))
        for lang_file in ['en.json', 'id.json']:
            lang_code = lang_file.split('.')[0]
            file_path = os.path.join(i18n_dir, lang_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"Error loading {lang_file}: {str(e)}")

    def get_text(self, key_path):
        """
        Get translated text using dot notation
        Example: get_text('login.like4like_cookies')
        """
        try:
            current_dict = self.translations[self.current_lang]
            for key in key_path.split('.'):
                current_dict = current_dict[key]
            return current_dict
        except (KeyError, TypeError):
            return f"Missing translation: {key_path}"

    def switch_language(self):
        """Switch between available languages"""
        self.current_lang = 'en' if self.current_lang == 'id' else 'id'
        return self.current_lang

    def get_current_language(self):
        """Get current language code"""
        return self.current_lang

# Create a singleton instance
i18n = I18nManager()