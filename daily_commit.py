from datetime import datetime
from git_utils import perform_commit

# Get today's date and perform commit
today = datetime.now()
date_string = perform_commit(today)
print(f"Commit completed with date: {date_string}")
