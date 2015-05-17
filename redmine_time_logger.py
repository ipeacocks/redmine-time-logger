'''
This script can count how many time need 
to be logged to each tickets for getting full month. 
Program uses Redmine REST API.
Author https://github.com/ipeacocks/redmine_time_logger
'''

from redmine import Redmine
from warnings import filterwarnings
from datetime import datetime, timedelta
import ConfigParser


# https://wiki.python.org/moin/ConfigParserExamples
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


# show all tickets from some date and return issue list (ids of problems)
def show_all_tickets():
    issue_list = []
    issues = REDMINE.issue.filter(status_id='*', created_on='>='+str(DATE_FOR_TICKET))
    for issue in issues:
        # we will not gather tickets with subtasks
        if not [subtask.id for subtask in issue.children]:
            issue_list.append(issue.id)
    return issue_list


def my_issues_and_time(issue_list):
    # total_time - total logged time for period
    total_time = 0
    last_issue_id = 0
    # list of issue numbers + data of time loggining
    # [(11308, datetime.date(2015, 4, 30)), (11994, datetime.date(2015, 4, 30))]
    my_issues = []

    #print issue_list

    for issue_id in issue_list:
        time_entries = (REDMINE.time_entry.filter(issue_id=issue_id, spent_on='>='+str(DATE)))
        #print dir(time_entries)

        try:
            for time_entry in time_entries:
                #print time_entry.hours
                if str(time_entry.user) == USERNAME:
                    #print issue_id, time_entry.hours
                    if issue_id != last_issue_id:
                        a = (issue_id, time_entry.spent_on)
                        my_issues.append(a)
                        last_issue_id = issue_id
                    total_time = total_time + time_entry.hours
                    # for debugging purposes
                    #print total_time, my_issues
                    #print len(my_issues), "- amount of tickets"
        except:
            pass

    time_to_log = work_time - total_time
    time_to_task = time_to_log/len(my_issues)
    # print time_to_task, my_issues, "time to each task + issue list with log time"
    return time_to_task, my_issues


def log_time(time_to_task, my_issues):
    for task_id, log_date in my_issues:
        issue = REDMINE.issue.get(task_id)
        # for debugging purposes
        print ("%s %s/issues/%s" % (issue, REDMINE_URL, task_id))
        print "Date for time log ", log_date
        print "Will be logged ", time_to_task
        print "-" * 80
        (REDMINE.time_entry.create(issue_id=task_id, spent_on=log_date, 
         hours=time_to_task, activity_id=17, comments=''))


Config = ConfigParser.ConfigParser()
Config.read("settings.ini")

REDMINE_URL = ConfigSectionMap("Address")['redmine_url']
REDMINE_KEY = ConfigSectionMap("Personal")['redmine_key']
USERNAME = ConfigSectionMap("Personal")['username']

# print REDMINE_URL, REDMINE_KEY, USERNAME
# DATE = '>=2014-10-01'
DATE = raw_input("From which date do you want to log time (format: year-month-day)? ")
work_time = float(raw_input("How many work hours in this month? "))

REDMINE = Redmine(REDMINE_URL, key=REDMINE_KEY, requests={'verify': False})

# ignore warning of request lib in case of bad cert on redmine
filterwarnings("ignore")

# http://stackoverflow.com/a/14459459/2971192
# We will search all tickets 10-20 days early
# because I could log time in old tickets.
DATE = datetime.strptime(DATE, "%Y-%m-%d").date()
# DATE_FOR_TICKET = DATE - relativedelta(months=1)
# was 30
DATE_FOR_TICKET = DATE-timedelta(days=10)

issue_list = show_all_tickets()
time_to_task, my_issues = my_issues_and_time(issue_list)
log_time(time_to_task, my_issues)