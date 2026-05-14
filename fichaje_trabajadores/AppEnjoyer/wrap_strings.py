import os
import re

TEMPLATE_DIR = 'app/templates'

def wrap_text(match):
    text = match.group(2).strip()
    if not text or '{' in text or '}' in text or '<' in text or '>' in text:
        return match.group(0)
    # Si ya está envuelto
    if text.startswith("{{ _(") or " _(" in text:
        return match.group(0)
    
    # Ignorar solo números o textos muy cortos sin letras
    if not re.search('[a-zA-Z]', text):
        return match.group(0)
        
    return f"{match.group(1)}{{{{ _('{text}') }}}}{match.group(3)}"

def wrap_placeholder(match):
    text = match.group(2).strip()
    if not text or '{' in text or '}' in text:
        return match.group(0)
    if text.startswith("{{ _("):
        return match.group(0)
    return f"{match.group(1)}{{{{ _('{text}') }}}}{match.group(3)}"

tags_to_wrap = ['label', 'button', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'th', 'a', 'span', 'p']

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for tag in tags_to_wrap:
        # Busca <tag ...>texto</tag>
        pattern = re.compile(f'(<{tag}[^>]*>)(.*?)(</{tag}>)', re.IGNORECASE | re.DOTALL)
        content = pattern.sub(wrap_text, content)
        
    # placeholders
    placeholder_pattern = re.compile(r'(placeholder=")(.*?)(")', re.IGNORECASE)
    content = placeholder_pattern.sub(wrap_placeholder, content)

    # title="" attributes
    title_pattern = re.compile(r'(title=")(.*?)(")', re.IGNORECASE)
    content = title_pattern.sub(wrap_placeholder, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Modificado: {filepath}")

for root, dirs, files in os.walk(TEMPLATE_DIR):
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))

print("Terminado.")
