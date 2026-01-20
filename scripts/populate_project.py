
import re

def parse_manual(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Regex to find tasks: "- [ ] Task Name" or "* [ ] Task Name"
    # Capturing the task description and the section header context if possible
    tasks = []
    
    # Split by lines to track context
    lines = content.split('\n')
    current_phase = "General"
    
    for line in lines:
        # Detect Phase Headers
        if line.startswith('### PHASE') or line.startswith('## '):
            current_phase = line.replace('#', '').strip()
        
        # Detect Checkboxes: Handles "* [ ] Task" and "* **[ ] Task**"
        match = re.search(r'^\s*[-*]\s*(?:\*\*)?\[\s*\](?:\*\*)?\s*(.+)', line)
        if match:
            task_desc = match.group(1).strip()
            # Clean up bolding markdown
            task_desc = task_desc.replace('**', '')
            tasks.append({
                'phase': current_phase,
                'title': task_desc
            })
            
    return tasks

def generate_gh_commands(tasks):
    print("# Copy and paste these lines into your terminal to create issues:")
    print("# Make sure you are logged in with 'gh auth login' first.")
    print("")
    
    for task in tasks:
        # Assign label based on phase
        label = "status:backlog"
        if "PHASE 1" in task['phase']: label = "phase:1-legal-shield"
        elif "PHASE 2" in task['phase']: label = "phase:2-paper-hub"
        elif "PHASE 3" in task['phase']: label = "phase:3-assets"
        elif "PHASE 4" in task['phase']: label = "phase:4-launch"
        
        # Escape quotes for shell safety
        title = task['title'].replace("'", "'\\''")
        
        # Construct command
        # Using --body to add context
        cmd = f"gh issue create --title '{title}' --body 'Derived from {task['phase']}' --label '{label}'"
        print(cmd)

if __name__ == "__main__":
    try:
        tasks = parse_manual('docs/MASTER_EXECUTION_FIELD_MANUAL.md')
        generate_gh_commands(tasks)
        print(f"\n# Successfully generated commands for {len(tasks)} tasks.")
    except FileNotFoundError:
        print("Error: Could not find docs/MASTER_EXECUTION_FIELD_MANUAL.md")
