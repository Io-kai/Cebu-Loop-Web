
import re
import urllib.parse

REPO_URL = "https://github.com/Io-kai/Cebu-Loop-Web/blob/main/docs/MASTER_EXECUTION_FIELD_MANUAL.md"

def slugify(text):
    # Convert "PHASE 1: THE LEGAL SHIELD..." to "phase-1-the-legal-shield..."
    # Markdown anchor logic: lowercase, replace spaces with dashes, remove punctuation
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

def parse_manual(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    tasks = []
    lines = content.split('\n')
    current_phase = "General"
    current_header_slug = ""
    
    for line in lines:
        # Detect Headers to build anchor links
        if line.startswith('### PHASE') or line.startswith('## '):
            current_phase = line.replace('#', '').strip()
            current_header_slug = slugify(current_phase)
        
        # Detect Checkboxes: Handles "* [ ] Task" and "* **[ ] Task**"
        match = re.search(r'^\s*[-*]\s*(?:\*\*)?\[\s*\](?:\*\*)?\s*(.+)', line)
        if match:
            task_desc = match.group(1).strip()
            task_desc = task_desc.replace('**', '') # Clean bold
            
            # Create deep link
            link = f"{REPO_URL}#{current_header_slug}"
            
            tasks.append({
                'phase': current_phase,
                'title': task_desc,
                'link': link
            })
            
    return tasks

def generate_gh_commands(tasks):
    print("# RELOAD SCRIPT (Run this to update your issues)")
    print("# This will create NEW issues. You may want to delete old ones first manually.")
    print("")
    
    for task in tasks:
        # Assign label based on phase
        label = "status:backlog"
        if "PHASE 1" in task['phase']: label = "phase:1-legal-shield"
        elif "PHASE 2" in task['phase']: label = "phase:2-paper-hub"
        elif "PHASE 3" in task['phase']: label = "phase:3-assets"
        elif "PHASE 4" in task['phase']: label = "phase:4-launch"
        elif "PHASE 0" in task['phase']: label = "phase:0-bag-builder"
        
        title = task['title'].replace("'", "'\\''")
        
        # Rich Body with Link
        body = f"**Source**: [{task['phase']}]({task['link']})\\n\\nContext: This task is part of the master execution timeline."
        
        cmd = f"gh issue create --title '{title}' --body '{body}' --label '{label}'"
        print(cmd)

if __name__ == "__main__":
    try:
        tasks = parse_manual('docs/MASTER_EXECUTION_FIELD_MANUAL.md')
        generate_gh_commands(tasks)
        print(f"\n# Successfully generated commands for {len(tasks)} tasks.")
    except FileNotFoundError:
        print("Error: Could not find docs/MASTER_EXECUTION_FIELD_MANUAL.md")
