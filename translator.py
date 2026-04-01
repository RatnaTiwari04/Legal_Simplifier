from googletrans import Translator

translator = Translator()

def detect_language(text):
    detected = translator.detect(text)
    return detected.lang

def translate_text(text, src_lang, dest_lang):
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated.text