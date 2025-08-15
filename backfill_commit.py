from datetime import datetime, timedelta
import time
from git_utils import perform_commit

def single_date_commit():
    """Handle single date commit"""
    date_input = input("Enter date in mm/dd/yyyy format: ")
    user_date = datetime.strptime(date_input, "%m/%d/%Y")
    date_string = perform_commit(user_date)
    print(f"Backfill commit completed with date: {date_string}")

def date_range_commit():
    """Handle date range commit"""
    start_date_input = input("Enter start date in mm/dd/yyyy format: ")
    end_date_input = input("Enter end date in mm/dd/yyyy format: ")
    
    start_date = datetime.strptime(start_date_input, "%m/%d/%Y")
    end_date = datetime.strptime(end_date_input, "%m/%d/%Y")
    
    current_date = start_date
    while current_date <= end_date:
        date_string = perform_commit(current_date)
        print(f"Commit completed for: {date_string}")
        current_date += timedelta(days=1)
        time.sleep(1)

# Menu
print("Backfill Commit Options:")
print("1. Single date commit")
print("2. Date range commit")
choice = input("Enter your choice (1 or 2): ")

if choice == "1":
    single_date_commit()
elif choice == "2":
    date_range_commit()
else:
    print("Invalid choice")
