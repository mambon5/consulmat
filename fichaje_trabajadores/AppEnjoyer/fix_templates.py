import os
import re

for root, _, files in os.walk('app/templates'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            # Replace { _('...') } with {{ _('...') }}
            new_content = re.sub(r'\{ _\(\'(.*?)\'\) \}', r"{{ _('\1') }}", content)
            
            # Also replace ones without spaces inside like {_('...')} if any
            new_content = re.sub(r'\{_\(\'(.*?)\'\)\}', r"{{ _('\1') }}", new_content)
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Fixed {path}")
