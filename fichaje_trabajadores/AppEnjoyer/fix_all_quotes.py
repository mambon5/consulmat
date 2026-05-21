import os
import re

TEMPLATE_DIR = 'app/templates'

def convert_quotes(content):
    pos = 0
    new_content = []
    n = len(content)
    modified = False

    while pos < n:
        # Match _( with optional whitespace, e.g., _( or _ (
        match = re.match(r'_\s*\(', content[pos:])
        if match:
            start_pos = pos
            pos += len(match.group(0))
            
            # Now we look at the quote character
            # Skip any whitespace inside _(
            while pos < n and content[pos].isspace():
                pos += 1
                
            if pos < n and content[pos] in ("'", '"'):
                quote_char = content[pos]
                pos += 1
                string_start = pos
                
                # Scan for the end of the string
                # The end is the next quote_char that is followed by optional whitespace and ')'
                end_quote_pos = -1
                scan_pos = pos
                while scan_pos < n:
                    if content[scan_pos] == quote_char:
                        # Check if it is followed by optional whitespace and ')'
                        rest = content[scan_pos + 1:]
                        closing_match = re.match(r'^\s*\)', rest)
                        if closing_match:
                            end_quote_pos = scan_pos
                            break
                    scan_pos += 1
                
                if end_quote_pos != -1:
                    string_content = content[string_start:end_quote_pos]
                    
                    # Process string content:
                    # 1. Unescape single quotes if they were escaped (e.g. \' -> ')
                    # 2. Escape double quotes (e.g. " -> \")
                    processed_content = string_content
                    # Unescape escaped single quotes: \' -> '
                    processed_content = processed_content.replace(r"\'", "'")
                    # Escape double quotes: " -> \", but don't double escape already escaped double quotes
                    # Let's do it safely:
                    # Temporary placeholder for existing \"
                    processed_content = processed_content.replace(r'\"', '___DBL_QUOTE___')
                    processed_content = processed_content.replace('"', r'\"')
                    processed_content = processed_content.replace('___DBL_QUOTE___', r'\"')
                    
                    # Now build the replacement
                    replacement = f'_("{processed_content}")'
                    
                    # Compute where the whole call ended: end_quote_pos + 1 (quote char) + len(closing_match.group(0)) (closing parenthesis and spaces)
                    end_call_pos = end_quote_pos + 1 + len(closing_match.group(0))
                    original_call = content[start_pos:end_call_pos]
                    
                    if original_call != replacement:
                        new_content.append(replacement)
                        modified = True
                    else:
                        new_content.append(original_call)
                    
                    pos = end_call_pos
                    continue
                else:
                    # If we couldn't find a proper end, revert back
                    new_content.append(content[start_pos:pos])
            else:
                new_content.append(content[start_pos:pos])
        else:
            new_content.append(content[pos])
            pos += 1

    return "".join(new_content), modified

def main():
    total_modified = 0
    for root, _, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content, modified = convert_quotes(content)
                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {filepath}")
                    total_modified += 1
                else:
                    print(f"No changes: {filepath}")
    print(f"Done. Modified {total_modified} files.")

if __name__ == '__main__':
    main()
