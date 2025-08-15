from datetime import datetime, timedelta
import time
from git_utils import extract_current_username, perform_commit, extract_commit

# Get all commit information
print("--------------------------------")
print("Extracing commit information...")
commits = extract_commit()
print(f"Extracted {len(commits)} commits")

def single_date_commit():
    """Handle single date commit"""
    try:
        date_input = input("Enter date in mm/dd/yyyy format: ")
        user_date = datetime.strptime(date_input, "%m/%d/%Y")
        date_string = perform_commit(user_date)
        print(f"Backfill commit completed with date: {date_string}")
    except ValueError:
        print("Error: Please enter the date in mm/dd/yyyy format (e.g., 12/25/2023)")
    except Exception as e:
        print(f"Error: {e}")

def date_range_commit():
    """Handle date range commit"""
    try:
        start_date_input = input("Enter start date in mm/dd/yyyy format: ")
        end_date_input = input("Enter end date in mm/dd/yyyy format: ")
        
        start_date = datetime.strptime(start_date_input, "%m/%d/%Y")
        end_date = datetime.strptime(end_date_input, "%m/%d/%Y")
        
        if start_date > end_date:
            print("Error: Start date cannot be after end date")
            return
        
        current_date = start_date
        while current_date <= end_date:
            date_string = perform_commit(current_date)
            print(f"Commit completed for: {date_string}")
            current_date += timedelta(days=1)
            time.sleep(1)
    except ValueError:
        print("Error: Please enter dates in mm/dd/yyyy format (e.g., 12/25/2023)")
    except Exception as e:
        print(f"Error: {e}")

def month_year_commit():
    """Handle month and year commit"""
    try:
        month_year_input = input("Enter month and year in mm/yyyy format: ")
        
        # Check if input contains exactly one '/'
        if month_year_input.count('/') != 1:
            print("Error: Please enter month and year in mm/yyyy format (e.g., 12/2023)")
            return
        
        # Parse month and year
        month, year = month_year_input.split('/')
        
        # Validate month and year are numeric
        if not month.isdigit() or not year.isdigit():
            print("Error: Month and year must be numbers")
            return
        
        month = int(month)
        year = int(year)
        
        # Validate month range
        if month < 1 or month > 12:
            print("Error: Month must be between 1 and 12")
            return
        
        # Validate year range (reasonable range)
        if year < 2000 or year > 2100:
            print("Error: Year must be between 2000 and 2100")
            return
        
        # Get current date
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
            # For current month, start from today and go backwards to first day
            if today.day == 1:
                # If today is the first day, only commit for today
                start_date = today
                end_date = today
                print(f"Today is the first day of {start_date.strftime('%B %Y')}. Backfilling commit for today only.")
            else:
                # Start from today and go backwards to first day of month
                start_date = datetime(year, month, 1)
                end_date = today
                print(f"Backfilling commits for current month {start_date.strftime('%B %Y')} from first day to today ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        else:
            # For past months, commit for the entire month
            print(f"Backfilling commits for {start_date.strftime('%B %Y')} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        
        current_date = start_date
        while current_date <= end_date:
            date_string = perform_commit(current_date)
            print(f"Commit completed for: {date_string}")
            current_date += timedelta(days=1)
            time.sleep(1)
    except ValueError as e:
        print(f"Error: Invalid date format. Please use mm/yyyy format (e.g., 12/2023)")
    except Exception as e:
        print(f"Error: {e}")

def month_year_commit_skip_existing():
    """Handle month and year commit with skip existing dates"""
    try:
        month_year_input = input("Enter month and year in mm/yyyy format: ")
        
        # Check if input contains exactly one '/'
        if month_year_input.count('/') != 1:
            print("Error: Please enter month and year in mm/yyyy format (e.g., 12/2023)")
            return
        
        # Parse month and year
        month, year = month_year_input.split('/')
        
        # Validate month and year are numeric
        if not month.isdigit() or not year.isdigit():
            print("Error: Month and year must be numbers")
            return
        
        month = int(month)
        year = int(year)
        
        # Validate month range
        if month < 1 or month > 12:
            print("Error: Month must be between 1 and 12")
            return
        
        # Validate year range (reasonable range)
        if year < 2000 or year > 2100:
            print("Error: Year must be between 2000 and 2100")
            return
        
        # Get current date
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
            # For current month, start from today and go backwards to first day
            if today.day == 1:
                # If today is the first day, only commit for today
                start_date = today
                end_date = today
                print(f"Today is the first day of {start_date.strftime('%B %Y')}. Backfilling commit for today only.")
            else:
                # Start from today and go backwards to first day of month
                start_date = datetime(year, month, 1)
                end_date = today
                print(f"Checking commits for current month {start_date.strftime('%B %Y')} from first day to today ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        else:
            # For past months, commit for the entire month
            print(f"Checking commits for {start_date.strftime('%B %Y')} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        
        # Extract existing commit dates
        print("Analyzing existing commits...")
        existing_dates = set()
        
        for commit in commits:
            try:
                # Parse the commit date
                commit_date = datetime.strptime(commit.date, "%a %b %d %H:%M:%S %Y %z")
                # Convert to date only for comparison
                commit_date_only = commit_date.date()
                
                # Check if this commit is within our target month/year
                if commit_date.year == year and commit_date.month == month:
                    existing_dates.add(commit_date_only)
            except ValueError:
                # Skip commits with unparseable dates
                continue
        
        # Find dates that need commits
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
        
        # Show skipped dates
        if skipped_dates:
            print(f"\nSkipped dates (already committed):")
            for date in sorted(skipped_dates):
                print(f"  - {date.strftime('%Y-%m-%d')}")
            print(f"Total skipped: {len(skipped_dates)} dates")
        
        # Show dates to commit
        if dates_to_commit:
            print(f"\nDates to commit:")
            for date in dates_to_commit:
                print(f"  - {date.strftime('%Y-%m-%d')}")
            print(f"Total to commit: {len(dates_to_commit)} dates")
        else:
            print("\nAll dates in this month already have commits!")
            return
        
        # Ask user if they want to continue
        print(f"\nDo you want to continue with committing {len(dates_to_commit)} dates?")
        continue_choice = input("Enter 'y' for yes, 'n' for no: ").lower().strip()
        
        if continue_choice != 'y':
            print("Operation cancelled. Returning to main menu.")
            return
        
        # Proceed with commits
        print(f"\nStarting commits for {len(dates_to_commit)} dates...")
        for i, date in enumerate(dates_to_commit, 1):
            date_string = perform_commit(date)
            print(f"Commit {i}/{len(dates_to_commit)} completed for: {date_string}")
            time.sleep(1)
        
        print(f"\nCompleted! Successfully committed {len(dates_to_commit)} dates.")
        
    except ValueError as e:
        print(f"Error: Invalid date format. Please use mm/yyyy format (e.g., 12/2023)")
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
print("3. Month and year commit")
print("4. Month and year commit (skip existing)")
choice = input("Enter your choice (1, 2, 3, or 4): ")

if choice == "1":
    single_date_commit()
elif choice == "2":
    date_range_commit()
elif choice == "3":
    month_year_commit()
elif choice == "4":
    month_year_commit_skip_existing()
else:
    print("Error: Please enter a valid choice (1, 2, 3, or 4)")
