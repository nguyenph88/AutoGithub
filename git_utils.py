import random
import subprocess
import os
from datetime import datetime

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

def perform_commit(date_obj):
    """Main function to perform the complete commit process"""
    date_string = create_date_string(date_obj)
    append_to_commit_file(date_string)
    run_git_commands(date_string)
    return date_string
