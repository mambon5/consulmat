import polib
from googletrans import Translator
import time
import os

translator = Translator()

def translate_po(filepath, dest_lang):
    po = polib.pofile(filepath)
    for entry in po.untranslated_entries():
        if not entry.msgid.strip():
            continue
        try:
            translation = translator.translate(entry.msgid, src='es', dest=dest_lang)
            entry.msgstr = translation.text
            print(f"Translated to {dest_lang}: {entry.msgid} -> {entry.msgstr}")
            time.sleep(0.5)  # Avoid rate limiting
        except Exception as e:
            print(f"Error translating {entry.msgid}: {e}")
            entry.msgstr = entry.msgid  # Fallback to original
    po.save()

# English
en_path = 'app/translations/en/LC_MESSAGES/messages.po'
if os.path.exists(en_path):
    translate_po(en_path, 'en')

# Catalan
ca_path = 'app/translations/ca/LC_MESSAGES/messages.po'
if os.path.exists(ca_path):
    translate_po(ca_path, 'ca')

# Spanish (Self)
es_path = 'app/translations/es/LC_MESSAGES/messages.po'
if os.path.exists(es_path):
    po = polib.pofile(es_path)
    for entry in po.untranslated_entries():
        entry.msgstr = entry.msgid
    po.save()

print("Translation completed.")
