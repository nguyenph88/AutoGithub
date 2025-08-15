import random
import subprocess
import os
import time
from datetime import datetime, timedelta
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

def perform_batch_commits(dates_to_commit, batch_size=10):
    """Perform commits in batches for better performance"""
    total_dates = len(dates_to_commit)
    print(f"Starting batch commits for {total_dates} dates (batch size: {batch_size})...")
    
    for i in range(0, total_dates, batch_size):
        batch = dates_to_commit[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_dates + batch_size - 1) // batch_size
        
        print(f"\nProcessing batch {batch_num}/{total_batches} ({len(batch)} dates)...")
        
        for j, date in enumerate(batch, 1):
            global_index = i + j
            date_string = perform_commit(date)
            print(f"Commit {global_index}/{total_dates} completed for: {date_string}")
            time.sleep(1)  # Keep 1-second delay between individual commits
        
        # Add a small delay between batches
        if i + batch_size < total_dates:
            print("Batch completed. Starting next batch...")
            time.sleep(2)
    
    print(f"\nAll {total_dates} commits completed successfully!")

def validate_date_input(date_input, format_type="mm/dd/yyyy"):
    """Validate date input format"""
    try:
        if format_type == "mm/dd/yyyy":
            return datetime.strptime(date_input, "%m/%d/%Y"), None
        elif format_type == "mm/yyyy":
            if date_input.count('/') != 1:
                return None, "Please enter month and year in mm/yyyy format (e.g., 12/2023)"
            
            month, year = date_input.split('/')
            if not month.isdigit() or not year.isdigit():
                return None, "Month and year must be numbers"
            
            month, year = int(month), int(year)
            if month < 1 or month > 12:
                return None, "Month must be between 1 and 12"
            if year < 2000 or year > 2100:
                return None, "Year must be between 2000 and 2100"
            
            return (month, year), None
        elif format_type == "yyyy":
            if not date_input.isdigit():
                return None, "Year must be a number"
            
            year = int(date_input)
            if year < 2000 or year > 2100:
                return None, "Year must be between 2000 and 2100"
            
            return year, None
    except ValueError:
        return None, f"Invalid date format. Please use {format_type} format"
    except Exception as e:
        return None, f"Error: {e}"

def get_date_range_for_month(month, year):
    """Get start and end dates for a given month/year"""
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    
    # Get the first day of the month
    start_date = datetime(year, month, 1)
    
    # Get the last day of the month
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Check if it's the current month and year
    if month == current_month and year == current_year:
        if today.day == 1:
            # If today is the first day, only commit for today
            start_date = today
            end_date = today
        else:
            # Start from first day of month to today
            end_date = today
    
    return start_date, end_date

def get_date_range_for_year(year):
    """Get start and end dates for a given year"""
    today = datetime.now()
    current_year = today.year
    
    # Get the first day of the year
    start_date = datetime(year, 1, 1)
    
    # Get the last day of the year
    end_date = datetime(year, 12, 31)
    
    # Check if it's the current year
    if year == current_year:
        # For current year, only commit up to today
        end_date = today
    
    return start_date, end_date

def analyze_existing_commits(commits, start_date, end_date, target_type="month", target_month=None, target_year=None):
    """Analyze existing commits and return existing dates set"""
    existing_dates = set()
    
    for commit in commits:
        try:
            # Parse the commit date
            commit_date = datetime.strptime(commit.date, "%a %b %d %H:%M:%S %Y %z")
            # Convert to date only for comparison
            commit_date_only = commit_date.date()
            
            # Check if this commit is within our target range
            if target_type == "month":
                if commit_date.year == target_year and commit_date.month == target_month:
                    existing_dates.add(commit_date_only)
            elif target_type == "year":
                if commit_date.year == target_year:
                    existing_dates.add(commit_date_only)
        except ValueError:
            # Skip commits with unparseable dates
            continue
    
    return existing_dates

def find_dates_to_commit(start_date, end_date, existing_dates):
    """Find dates that need commits and dates to skip"""
    dates_to_commit = []
    skipped_dates = []
    
    current_date = start_date
    while current_date <= end_date:
        current_date_only = current_date.date()
        if current_date_only in existing_dates:
            skipped_dates.append(current_date_only)
        else:
            dates_to_commit.append(current_date)
        current_date += timedelta(days=1)
    
    return dates_to_commit, skipped_dates

def display_commit_summary(skipped_dates, dates_to_commit, limit_display=20):
    """Display summary of skipped and to-commit dates"""
    # Show skipped dates
    if skipped_dates:
        if len(skipped_dates) > limit_display:
            print(f"\nSkipped dates (already committed) - showing first {limit_display}:")
            for date in sorted(skipped_dates)[:limit_display]:
                print(f"  - {date.strftime('%Y-%m-%d')}")
            print(f"  ... and {len(skipped_dates) - limit_display} more dates")
        else:
            print(f"\nSkipped dates (already committed):")
            for date in sorted(skipped_dates):
                print(f"  - {date.strftime('%Y-%m-%d')}")
        print(f"Total skipped: {len(skipped_dates)} dates")
    
    # Show dates to commit
    if dates_to_commit:
        if len(dates_to_commit) > limit_display:
            print(f"\nDates to commit - showing first {limit_display}:")
            for date in dates_to_commit[:limit_display]:
                print(f"  - {date.strftime('%Y-%m-%d')}")
            print(f"  ... and {len(dates_to_commit) - limit_display} more dates")
        else:
            print(f"\nDates to commit:")
            for date in dates_to_commit:
                print(f"  - {date.strftime('%Y-%m-%d')}")
        print(f"Total to commit: {len(dates_to_commit)} dates")
    else:
        print("\nAll dates already have commits!")
        return False
    
    return True

def execute_commits(dates_to_commit):
    """Execute commits with appropriate processing method"""
    if len(dates_to_commit) > 10:
        # Use batch processing for large numbers of commits
        # Calculate optimal batch size: minimum of 10 or total_dates/5, but at least 5
        batch_size = max(5, min(10, len(dates_to_commit) // 5))
        perform_batch_commits(dates_to_commit, batch_size)
    else:
        # Use regular processing for smaller numbers
        print(f"\nStarting commits for {len(dates_to_commit)} dates...")
        for i, date in enumerate(dates_to_commit, 1):
            date_string = perform_commit(date)
            print(f"Commit {i}/{len(dates_to_commit)} completed for: {date_string}")
            time.sleep(1)
        print(f"\nCompleted! Successfully committed {len(dates_to_commit)} dates.")

def show_greedy_warning():
    """Show warning for greedy commit operations"""
    print("\n⚠️  WARNING: This option will commit on ALL dates,")
    print("   including dates that already have commits (greedy commit).")
    print("   This may create duplicate commits for the same date.")
    
    confirm = input("\nDo you want to continue? (y/n): ").lower().strip()
    return confirm == 'y'

def get_user_confirmation(message):
    """Get user confirmation for an operation"""
    print(f"\n{message}")
    continue_choice = input("Enter 'y' for yes, 'n' for no: ").lower().strip()
    return continue_choice == 'y'


