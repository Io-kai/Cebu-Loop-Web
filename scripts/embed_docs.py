import os
import re

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
INDEX_PATH = os.path.join(DOCS_DIR, 'index.html')
MANUAL_PATH = os.path.join(DOCS_DIR, 'MASTER_EXECUTION_FIELD_MANUAL.md')
LOG_PATH = os.path.join(DOCS_DIR, 'CRITICAL_DECISIONS_LOG.md')

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return ""

def embed_content(html_content, script_id, md_content):
    # Regex to find the script tag content
    # Look for <script id="script_id" type="text/markdown"> ... </script>
    pattern = f'(<script id="{script_id}" type="text/markdown">)(.*?)(</script>)'
    
    # Escape any existing </script> tags in the markdown content to prevent breaking HTML
    # Although markdown usually uses code blocks, we should be careful.
    # A simple trick is to replace </script> with <\/script> inside text strings,
    # but since this is raw text node, looking for the tag is enough.
    # We will assume standard markdown doesn't contain raw </script> tags.
    
    # We use DOTALL to match newlines
    replacement = f'\\1\n{md_content}\n\\3'
    
    new_content = re.sub(pattern, lambda m: f'{m.group(1)}\n{md_content}\n{m.group(3)}', html_content, flags=re.DOTALL)
    return new_content

def main():
    print(f"Reading HTML from {INDEX_PATH}...")
    html_content = read_file(INDEX_PATH)
    
    if not html_content:
        return

    print("Reading Docs...")
    manual_content = read_file(MANUAL_PATH)
    decision_content = read_file(LOG_PATH)
    
    print(f"Embedding Manual ({len(manual_content)} bytes)...")
    html_content = embed_content(html_content, 'raw-manual', manual_content)
    
    print(f"Embedding Decision Log ({len(decision_content)} bytes)...")
    html_content = embed_content(html_content, 'raw-decisions', decision_content)
    
    print("Writing updated index.html...")
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("Success! Documentation embedded.")

if __name__ == "__main__":
    main()
