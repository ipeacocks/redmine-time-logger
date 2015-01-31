This script can search all your tickets which you was involved in during month and log time there.
It can be usefull in the end of month because manual time loggining is pretty annoying. 

Script produces such output:

```bash
$ python redmine_time_logger.py
From which date do you want to log time (format: year-month-day)? 2015-01-01
[Download App]: Error downloading files [https://redmine.example.com/issues/1345309]
Logged 1.1 hours
---
Provide SSH access to server for John Dou [https://redmine.example.com/issues/1345310]
Logged 0.8 hours
---
```

I use this library http://python-redmine.readthedocs.org/
Ask me if you have any questions