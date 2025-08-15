from datetime import datetime
from git_utils import perform_commit

# Get user input for date
date_input = input("Enter date in mm/dd/yyyy format: ")
user_date = datetime.strptime(date_input, "%m/%d/%Y")

# Perform commit with user-specified date
date_string = perform_commit(user_date)
print(f"Backfill commit completed with date: {date_string}")
