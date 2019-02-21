This script can search all your tickets which you was involved in during month and log time there for getting month norm.
It can be usefull in the end of month because manual time loggining is quite annoying. 

```
time_to_ticket = (month_norm - logged_time) / amount_of_tickets
```

so **time_to_ticket** will be logged to each ticket for getting norm.

Script produces such output:

```
» python redmine_time_logger.py
From which date do you want to log time (format: year-month-day)? 2015-01-01
How many work hours in this month? 160
--------------------------------------------------------------------------------
New instance html-menu https://type.your-address.com/issues/11457
Date for time log  2015-01-15
Will be logged  11.2046153846
--------------------------------------------------------------------------------
...
--------------------------------------------------------------------------------
[Admin] Git access https://type.your-address.com/issues/11456
Date for time log  2015-01-15
Will be logged  11.2046153846
--------------------------------------------------------------------------------
Access to git@git.my.com:test refused https://type.your-address.com/issues/11446
Date for time log  2015-01-14
Will be logged  11.2046153846
--------------------------------------------------------------------------------
```

I use this library https://github.com/maxtepkeev/python-redmine

Ask me if you have any questions
