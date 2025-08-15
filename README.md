AutoGithub
==========

Want your Github's activity looks something cool like this? This tool will help :)

Note: 
- I only provide tool to commit, how to uncommit if you made a mistake, it's up to you.
- For education purpose and my use only, I'm not responsible for what happened to your github or repo or commit if you use this.
- I'm NOT using the github API, not comfortable doing that.

![Image](demo.png?raw=true)

Legacy v1
---------------
Yup, I created v1 12 years ago while I was in college. It's "legacy" and I marked that as v1.0.0. Feel free to check that out, it may work (or not) using PHP and curl


New V2 (2025)
---------------
Simple script to help you fill your daily commit schedule chart and make it colorful on github :)

How to use:
- Run `py daily_commit.py` it will commit the message for today
- If you want to set it up to run daily, see the Scheduled Task as below

What is `backfill_commit.py`?
---------------
So you missed your commit and fill for the whole year, or just want to fill it for a specific day/month? Use this file.

![Image](backfill.png?raw=true)

- Run `py backfill_commit.py`

How To Make It Run Automatically As Schedule (optional)
----------------
So of course as I usually do, I will take advantage of the automation process to make it run as scheduled.

For Windows:
- Use Task Scheduler to run `task_windows.bat` daily

For Linux:
- Use cron job to run `task_nix.sh` daily