import random
import subprocess
from datetime import datetime
import time

# Generate random time between 01:00:00 and 23:00:00
hour = random.randint(1, 23)
minute = random.randint(0, 59)
second = random.randint(0, 59)

# Create date string in PST timezone
today = datetime.now()
date_string = today.replace(hour=hour, minute=minute, second=second, microsecond=0).strftime("%a %d %b %Y %H:%M:%S PST")

# Add date string to commit.txt
with open('commit.txt', 'a') as f:
    f.write(date_string + '\n')

# Run git commands
subprocess.run(['git', 'add', 'commit.txt'])
subprocess.run(['git', 'commit', '--date', date_string, '-m', date_string])
subprocess.run(['git', 'push'])
