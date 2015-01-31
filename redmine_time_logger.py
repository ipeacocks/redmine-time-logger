'''
This script can log 0.7-1.2h of time for all tickets which
I was involved in and work only with Redmine and uses Redmine REST API.
'''

from redmine import Redmine
from warnings import filterwarnings
from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
import random


REDMINE_URL = 'https://redmine.example.com'
REDMINE_KEY = '9c68f1d5881_your_key_from_Redmine_f76d4bb97e246'
DATE = raw_input("From which date do you want to log time \
(format: year-month-day)? ")


# REDMINE = Redmine('https://redmine.example.com/', username='vpupkin',
# password='12345', requests={'verify': False})
REDMINE = Redmine(REDMINE_URL, key=REDMINE_KEY, requests={'verify': False})

# ignore warning of requests lib in case of bad cert on redmine
filterwarnings("ignore")

# http://stackoverflow.com/a/14459459/2971192
# We will search all tickets 1(2) months early
# because I could log time in old tickets.
DATE = datetime.strptime(DATE, "%Y-%m-%d").date()
# DATE_FOR_TICKET = DATE - relativedelta(months=1)
DATE_FOR_TICKET = DATE-timedelta(days=30)


# for usable output
def print_line():
    print '-' * 130


# show all tickets from some date and return issue list (ids of problems)
def show_all_tickets():
    issue_list = []
    issues = (REDMINE.issue.filter(status_id='*',
              created_on='>='+str(DATE_FOR_TICKET)))
    for issue in issues:
        # Epic ticket is bundle of tickets for usable monitoring
        if str(issue.tracker) != 'Epic' and 'EPIC' not in str(issue):
            issue_list.append(issue.id)

    # print issue_list
    return issue_list


# log time if I logged time early
def log_time(issue_list):
    counter = 0
    sum_time = 0
    for issue_id in issue_list:
        time_entries = (REDMINE.time_entry.filter(issue_id=issue_id,
                        spent_on='>='+str(DATE)))
        try:
            for time_entry in time_entries:
                # We are loggining time only for tickets where we was involved.
                if str(time_entry.user) == "User Name":
                    counter = counter + 1
                    hours = '%3.1f' % random.uniform(0.7, 1.2)
                    issue = REDMINE.issue.get(issue_id)
                    print ("%s [%s/issues/%s]" % (issue, REDMINE_URL,
                           str(issue_id)))
                    # print issue.tracker,"|"
                    # Time entries creating.
                    (REDMINE.time_entry.create(issue_id=issue_id,
                     spent_on=time_entry.spent_on, hours=hours,
                     activity_id=18, comments=''))
                    print "Logged %s hours" % hours
                    print "---"
                    sum_time = sum_time + float(hours)
                    break
        except:
            pass
    print "------------------------------------------"
    print "You were worked on %s tasks" % counter
    print "Total logged hours: %s" % sum_time

issue_list = show_all_tickets()
log_time(issue_list)
