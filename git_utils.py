import random
import subprocess
import os
from datetime import datetime
from dataclasses import dataclass

@dataclass
class GitLog:
    """Data structure for Git log entries"""
    commit: str
    author: str
    date: str

def generate_random_time():
    """Generate random time between 01:00:00 and 23:00:00"""
    hour = random.randint(1, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return hour, minute, second

def create_date_string(date_obj):
    """Create date string in PST format with random time"""
    hour, minute, second = generate_random_time()
    date_string = date_obj.replace(hour=hour, minute=minute, second=second, microsecond=0).strftime("%a %d %b %Y %H:%M:%S PST")
    return date_string

def append_to_commit_file(date_string):
    """Add date string to commit.txt file"""
    # Check file size (10KB = 10240 bytes)
    try:
        file_size = os.path.getsize('commit.txt')
        if file_size > 10240:  # 10KB
            # Empty the file and write at beginning
            with open('commit.txt', 'w') as f:
                f.write(date_string + '\n')
        else:
            # Append to existing content
            with open('commit.txt', 'a') as f:
                f.write(date_string + '\n')
    except FileNotFoundError:
        # File doesn't exist, create it
        with open('commit.txt', 'w') as f:
            f.write(date_string + '\n')

def run_git_commands(date_string):
    """Run git add, commit, and push commands"""
    subprocess.run(['git', 'add', 'commit.txt'])
    subprocess.run(['git', 'commit', '--date', date_string, '-m', date_string])
    subprocess.run(['git', 'push'])

def extract_current_username():
    """Extract username from git remote URL"""
    result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
    output = result.stdout
    # Extract URL from output (format: origin  https://github.com/username/repo.git (fetch))
    lines = output.strip().split('\n')
    if lines:
        url_line = lines[0]
        # Extract URL part
        url = url_line.split()[1]
        # Extract username from URL (https://github.com/username/repo.git)
        username = url.split('/')[-2]
        return username
    return None

def extract_commit():
    """Extract commit information from git log"""
    try:
        # Run git log command with specific format
        result = subprocess.run(['git', 'log', '--pretty=format:commit %H%nAuthor: %an%nDate: %ad%n'], 
                               capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error running git log: {result.stderr}")
            return []
        
        output = result.stdout.strip()
        if not output:
            return []
        
        # Parse the output
        git_logs = []
        lines = output.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for commit line
            if line.startswith('commit '):
                commit_hash = line[7:]  # Remove 'commit ' prefix
                
                # Get author (next line should start with 'Author: ')
                i += 1
                if i < len(lines) and lines[i].strip().startswith('Author: '):
                    author = lines[i].strip()[8:]  # Remove 'Author: ' prefix
                else:
                    author = "Unknown"
                
                # Get date (next line should start with 'Date: ')
                i += 1
                if i < len(lines) and lines[i].strip().startswith('Date: '):
                    date = lines[i].strip()[6:]  # Remove 'Date: ' prefix
                else:
                    date = "Unknown"
                
                # Create GitLog object
                git_log = GitLog(commit=commit_hash, author=author, date=date)
                git_logs.append(git_log)
            
            i += 1
        
        return git_logs
        
    except Exception as e:
        print(f"Error extracting commit dates: {e}")
        return []

def perform_commit(date_obj):
    """Main function to perform the complete commit process"""
    date_string = create_date_string(date_obj)
    append_to_commit_file(date_string)
    run_git_commands(date_string)
    return date_string
