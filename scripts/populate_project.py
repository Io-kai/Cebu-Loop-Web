import re
import urllib.parse
import sys
import subprocess
import json
import argparse
import time

REPO_URL = "https://github.com/Io-kai/Cebu-Loop-Web/blob/main/docs/MASTER_EXECUTION_FIELD_MANUAL.md"
MANUAL_PATH = 'docs/MASTER_EXECUTION_FIELD_MANUAL.md'

REQUIRED_LABELS = {
    "phase:0-bag-builder": "94A3B8",
    "phase:1-legal-shield": "EF4444",
    "phase:2-paper-hub": "F59E0B",
    "phase:3-assets": "F97316",
    "phase:4-launch": "10B981",
    "status:backlog": "D3D3D3"
}

def run_command(cmd, dry_run=False, print_only=False):
    if print_only:
        print(f"{' '.join(cmd)}")
        return None
    
    if dry_run:
        print(f"[DRY RUN] Would execute: {' '.join(cmd)}")
        return None

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(cmd)}")
        print(f"Stderr: {e.stderr}")
        return None

def ensure_labels_exist(dry_run=False, print_only=False):
    print("Checking labels...")
    if print_only:
        return

    existing_labels = []
    if not dry_run:
        try:
            output = run_command(["gh", "label", "list", "--json", "name"], dry_run=False)
            if output:
                existing_labels = [l['name'] for l in json.loads(output)]
        except Exception as e:
            print(f"Warning: Could not fetch existing labels: {e}")

    for name, color in REQUIRED_LABELS.items():
        if name not in existing_labels:
            print(f"Creating missing label: {name}")
            run_command(["gh", "label", "create", name, "--color", color, "--force"], dry_run=dry_run)
        else:
            print(f"Label '{name}' already exists.")

def delete_all_issues(dry_run=False, print_only=False):
    print("Deleting ALL existing issues...")
    if print_only:
        return

    issues = []
    if not dry_run:
        try:
            output = run_command(["gh", "issue", "list", "--state", "all", "--limit", "1000", "--json", "number"], dry_run=False)
            if output:
                issues = json.loads(output)
        except Exception as e:
            print(f"Error fetching issues: {e}")
            return

    if not issues:
        print("No issues found to delete.")
        return

    print(f"Found {len(issues)} issues to delete.")
    for issue in issues:
        num = str(issue['number'])
        print(f"Deleting issue #{num}...")
        run_command(["gh", "issue", "delete", num, "--yes"], dry_run=dry_run)

def slugify(text):
    # Convert "PHASE 1: THE LEGAL SHIELD..." to "phase-1-the-legal-shield..."
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
    
    current_task = None

    for line in lines:
        # Detect Headers to build anchor links
        if line.startswith('### PHASE') or line.startswith('## ') or line.startswith('#### '):
            if current_task:
                 tasks.append(current_task)
                 current_task = None
            
            if line.strip():
                # Only update phase if it's a phase header, not subheader?
                # Actually, we want the phase context. 
                # Let's keep it simple: if it says PHASE, grab it.
                if "PHASE" in line:
                    current_phase = line.replace('#', '').strip()
                    current_header_slug = slugify(current_phase)
            continue
        
        # Detect Checkboxes: Handles "* [ ] Task" and "* **[ ] Task**"
        match = re.search(r'^\s*[-*]\s*(?:\*\*)?\[\s*\](?:\*\*)?\s*(.+)', line)
        if match:
            # If we were building a previous task, save it
            if current_task:
                tasks.append(current_task)

            task_desc = match.group(1).strip()
            task_desc = task_desc.replace('**', '') # Clean bold
            
            # Create deep link
            # Note: current_header_slug might be stale if we are deep in subheaders,
            # but usually the anchors are on headings.
            link = f"{REPO_URL}#{current_header_slug}"
            
            current_task = {
                'phase': current_phase,
                'title': task_desc,
                'link': link,
                'body': []
            }
        elif current_task and line.strip():
             # Heuristic: If it has indentation, it belongs to the task.
            if line.startswith('  ') or line.startswith('\t'):
                current_task['body'].append(line.strip())

    if current_task:
        tasks.append(current_task)
            
    return tasks

def create_issues(tasks, dry_run=False, print_only=False):
    print(f"Creating {len(tasks)} issues...")
    
    for task in tasks:
        # Assign label based on phase
        label = "status:backlog"
        if "PHASE 1" in task['phase'].upper(): label = "phase:1-legal-shield"
        elif "PHASE 2" in task['phase'].upper(): label = "phase:2-paper-hub"
        elif "PHASE 3" in task['phase'].upper(): label = "phase:3-assets"
        elif "PHASE 4" in task['phase'].upper(): label = "phase:4-launch"
        elif "PHASE 0" in task['phase'].upper(): label = "phase:0-bag-builder"
        
        title = task['title']
        
        # Construct Rich Body
        body_lines = [f"**Source**: [{task['phase']}]({task['link']})\n"]
        body_lines.append("### Instructions")
        if task['body']:
            for line in task['body']:
                body_lines.append(f"{line}") # Already bulleted usually
        else:
             body_lines.append("No specific sub-instructions found in manual.")
        
        body_lines.append(f"\nContext: This task is part of the master execution timeline.")

        body = "\n".join(body_lines)
        
        cmd = [
            "gh", "issue", "create",
            "--title", title,
            "--body", body,
            "--label", label
        ]
        
        run_command(cmd, dry_run=dry_run, print_only=print_only)
        
        if not dry_run and not print_only:
             # Basic rate limiting to avoid tripping GitHub spam filters too hard
            time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="Populate GitHub project issues from manual.")
    parser.add_argument("--clean", action="store_true", help="Delete ALL existing issues before populating.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without doing it.")
    parser.add_argument("--print-only", action="store_true", help="Print commands to stdout instead of executing (for piping).")
    
    args = parser.parse_args()

    # Normal execution flow
    try:
        if args.clean:
            delete_all_issues(dry_run=args.dry_run, print_only=args.print_only)

        ensure_labels_exist(dry_run=args.dry_run, print_only=args.print_only)

        tasks = parse_manual(MANUAL_PATH)
        create_issues(tasks, dry_run=args.dry_run, print_only=args.print_only)
        
        if not args.dry_run and not args.print_only:
            print(f"\nSuccessfully processed {len(tasks)} tasks.")
            
    except FileNotFoundError:
        print(f"Error: Could not find {MANUAL_PATH}")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()
