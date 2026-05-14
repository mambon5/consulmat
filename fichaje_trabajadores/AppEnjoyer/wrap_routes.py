import os
import re

for root, _, files in os.walk('app/routes'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            original = content
            
            # Wrap flash('message', 'category')
            # But we must add from flask_babel import _ if it's used
            content = re.sub(r'flash\(\s*[\'"](.*?)[\'"]\s*,', r"flash(_('\1'),", content)
            
            # Also simple flash('message')
            content = re.sub(r'flash\(\s*[\'"](.*?)[\'"]\s*\)', r"flash(_('\1'))", content)

            if content != original:
                # Add import if not exists
                if 'from flask_babel import _' not in content:
                    content = "from flask_babel import _\n" + content
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Wrapped flash in {path}")
