from git_utils import extract_commit_date

# Get all commit information
commits = extract_commit_date()

# Access individual commit data
for commit in commits[:5]:  # First 5 commits
    print(f"Commit: {commit.commit}")
    print(f"Author: {commit.author}")
    print(f"Date: {commit.date}")
    print()