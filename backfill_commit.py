from datetime import datetime, timedelta
import time
from git_utils import (
    extract_current_username, perform_commit, extract_commit,
    validate_date_input, get_date_range_for_month, get_date_range_for_year,
    analyze_existing_commits, find_dates_to_commit, display_commit_summary,
    execute_commits, show_greedy_warning, get_user_confirmation
)

# Get all commit information
print("--------------------------------")
print("Extracting commit information...")
commits = extract_commit()
print(f"Extracted {len(commits)} commits")

def single_date_commit():
    """Handle single date commit"""
    try:
        date_input = input("Enter date in mm/dd/yyyy format: ")
        user_date, error = validate_date_input(date_input, "mm/dd/yyyy")
        
        if error:
            print(f"Error: {error}")
            return
        
        date_string = perform_commit(user_date)
        print(f"Backfill commit completed with date: {date_string}")
    except Exception as e:
        print(f"Error: {e}")

def date_range_commit():
    """Handle date range commit"""
    try:
        start_date_input = input("Enter start date in mm/dd/yyyy format: ")
        end_date_input = input("Enter end date in mm/dd/yyyy format: ")
        
        start_date, error = validate_date_input(start_date_input, "mm/dd/yyyy")
        if error:
            print(f"Error: {error}")
            return
        
        end_date, error = validate_date_input(end_date_input, "mm/dd/yyyy")
        if error:
            print(f"Error: {error}")
            return
        
        if start_date > end_date:
            print("Error: Start date cannot be after end date")
            return
        
        total_days = (end_date - start_date).days + 1
        print(f"Starting commits for {total_days} days...")
        
        current_date = start_date
        completed = 0
        
        while current_date <= end_date:
            completed += 1
            date_string = perform_commit(current_date)
            print(f"Commit {completed}/{total_days} completed for: {date_string}")
            current_date += timedelta(days=1)
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

def month_year_commit():
    """Handle month and year commit (greedy)"""
    try:
        if not show_greedy_warning():
            print("Operation cancelled. Returning to main menu.")
            return
        
        month_year_input = input("Enter month and year in mm/yyyy format: ")
        parsed_input, error = validate_date_input(month_year_input, "mm/yyyy")
        
        if error:
            print(f"Error: {error}")
            return
        
        month, year = parsed_input
        start_date, end_date = get_date_range_for_month(month, year)
        
        print(f"Backfilling commits for {start_date.strftime('%B %Y')} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        
        total_days = (end_date - start_date).days + 1
        print(f"Starting commits for {total_days} days...")
        
        current_date = start_date
        completed = 0
        
        while current_date <= end_date:
            completed += 1
            date_string = perform_commit(current_date)
            print(f"Commit {completed}/{total_days} completed for: {date_string}")
            current_date += timedelta(days=1)
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

def month_year_commit_skip_existing():
    """Handle month and year commit with skip existing dates"""
    try:
        month_year_input = input("Enter month and year in mm/yyyy format: ")
        parsed_input, error = validate_date_input(month_year_input, "mm/yyyy")
        
        if error:
            print(f"Error: {error}")
            return
        
        month, year = parsed_input
        start_date, end_date = get_date_range_for_month(month, year)
        
        print(f"Checking commits for {start_date.strftime('%B %Y')} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        
        # Analyze existing commits
        print("Analyzing existing commits...")
        existing_dates = analyze_existing_commits(commits, start_date, end_date, "month", month, year)
        
        # Find dates to commit
        dates_to_commit, skipped_dates = find_dates_to_commit(start_date, end_date, existing_dates)
        
        # Display summary
        if not display_commit_summary(skipped_dates, dates_to_commit):
            return
        
        # Get user confirmation
        if not get_user_confirmation(f"Do you want to continue with committing {len(dates_to_commit)} dates?"):
            print("Operation cancelled. Returning to main menu.")
            return
        
        # Execute commits
        execute_commits(dates_to_commit)
        
    except Exception as e:
        print(f"Error: {e}")

def year_commit():
    """Handle year commit (greedy)"""
    try:
        if not show_greedy_warning():
            print("Operation cancelled. Returning to main menu.")
            return
        
        year_input = input("Enter year (yyyy format): ")
        year, error = validate_date_input(year_input, "yyyy")
        
        if error:
            print(f"Error: {error}")
            return
        
        start_date, end_date = get_date_range_for_year(year)
        
        print(f"Backfilling commits for year {year} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        
        total_days = (end_date - start_date).days + 1
        print(f"Starting commits for {total_days} days...")
        
        current_date = start_date
        completed = 0
        
        while current_date <= end_date:
            completed += 1
            date_string = perform_commit(current_date)
            print(f"Commit {completed}/{total_days} completed for: {date_string}")
            current_date += timedelta(days=1)
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

def year_commit_skip_existing():
    """Handle year commit with skip existing dates"""
    try:
        year_input = input("Enter year (yyyy format): ")
        year, error = validate_date_input(year_input, "yyyy")
        
        if error:
            print(f"Error: {error}")
            return
        
        start_date, end_date = get_date_range_for_year(year)
        
        print(f"Checking commits for year {year} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        
        # Analyze existing commits
        print("Analyzing existing commits...")
        existing_dates = analyze_existing_commits(commits, start_date, end_date, "year", target_year=year)
        
        # Find dates to commit
        dates_to_commit, skipped_dates = find_dates_to_commit(start_date, end_date, existing_dates)
        
        # Display summary
        if not display_commit_summary(skipped_dates, dates_to_commit):
            return
        
        # Get user confirmation
        if not get_user_confirmation(f"Do you want to continue with committing {len(dates_to_commit)} dates?"):
            print("Operation cancelled. Returning to main menu.")
            return
        
        # Execute commits
        execute_commits(dates_to_commit)
        
    except Exception as e:
        print(f"Error: {e}")

# Menu
print("--------------------------------")
print(f"Current username: {extract_current_username()}")
print(f"Current date: {datetime.now().strftime('%Y-%m-%d')}")
print("If this is not your current date or username, make sure you are at the right repo")
print("--------------------------------")
print("Backfill Commit Options:")
print("1. Single date commit")
print("2. Date range commit")
print("3. Month and year commit (greedy commit)")
print("4. Month and year commit (skip existing)")
print("5. Year commit (greedy commit)")
print("6. Year commit (skip existing)")
choice = input("Enter your choice (1, 2, 3, 4, 5, or 6): ")

if choice == "1":
    single_date_commit()
elif choice == "2":
    date_range_commit()
elif choice == "3":
    month_year_commit()
elif choice == "4":
    month_year_commit_skip_existing()
elif choice == "5":
    year_commit()
elif choice == "6":
    year_commit_skip_existing()
else:
    print("Error: Please enter a valid choice (1, 2, 3, 4, 5, or 6)")
