AutoGithub
==========

Want your Github's activity looks something cool like this? This tool will help :)

![Image](demo.png?raw=true)

Notice
---------------
Since Github has updated the way their API needs to be accessed and authenticated, the tool doesn't work anymore but you can feel free to look at their API and manupulate around the problem. They somehow removed my demo account so use at your own risk.


How It Works
---------------
The concept is very simple, you need to create a temp repo which a temp file in it (eg: README.md). By using Github API, you can be able to connect to the API service, browse the file, update which a particular (random) content/message, commit and push it back. The process will count as 1 commit to the graph above and the color of that current date will be updated also. (remember to update everythin inside the file, also the blob)

You can test it locally first and upload it the the website for mobile access. Every time you want to run the script then just visit www.yourwebsite.com/autogithub.php and the script will do the job.

How To Make It Run Automatically As Schedule
----------------
So of course as I usually do, I will take advantage of the automation process to make it run as scheduled.

The reason why I use PHP is because for most of the web hosting service, they will support PHP along with cPanel. Inside the cPanel you will find a function called "Schedule Cronjob", read more about how to script that file then ultiize the file to make your web hosting run that particular file as schedule. (For me, I set it to run every) Beside, cURL also works for PHP.

    Eg (cronjob): php /home/USER/public_html/autogithub.php
    Eg (cURL): curl http://www.yourwebsite.com/autogithub.php

You can use other languages like Java, C or NodeJS to access the API and do as above. But it's hard to find a web service that support cronjob for those. Heroku charges 2 dyno for it Scheduler (https://devcenter.heroku.com/articles/scheduler). That's the main reason I stick with PHP and Cpanel's Cronjob.

