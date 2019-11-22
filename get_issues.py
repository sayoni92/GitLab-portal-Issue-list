#!/usr/bin/env python3

import json
import requests
import os
from datetime import datetime
from datetime import time
from numpy import busday_count
from business_duration import businessDuration
import holidays as pyholidays
from openpyxl import Workbook

def to_date(dt):
    return datetime.strptime(dt,'%Y-%m-%dT%H:%M:%S.%fZ')

def datestr(dt):
    if dt is None:
        return ''
    else:
        return datetime.strftime(dt,'%Y-%m-%d %H:%M:%S.%f')

def businesshours(start, end):
    US_holiday_list = pyholidays.US(state='NY')
    biz_open_time=time(8,0,0)
    biz_close_time=time(17,0,0)
    unit_hour='hour'
    return businessDuration(startdate=start,enddate=end,starttime=biz_open_time,endtime=biz_close_time,holidaylist=US_holiday_list,unit=unit_hour)

PROJ='8352981'
#ISSUES_URL= ' Please use your own URL  '  
HEADER={'PRIVATE-TOKEN': os.environ['GITLAB_IssuesExport']}

r = requests.get(ISSUES_URL, headers=HEADER)
issues = json.loads(r.text)

wb = Workbook()
ws = wb.active
r = ['title','created_at','updated_at','closed_at','Spent','Estimated','note_count','note_id','note_created','last_date','note_person','assigned','lapse_hrs','bizlapse_hrs','is_response','is_bug','is_support','is_kt', 'is_hi', 'is_med', 'is_low','is_enhancement','in_progress','ready_for_review','is_open']
ws.append(r)
print('|'.join(r))

for i in issues:
    title = i['title']
    created_at = to_date(i['created_at'])
    updated_at = to_date(i['updated_at'])
    
    try:
        closed_at = to_date(i['closed_at'])
    except:
        closed_at = None
    
    Spent = i['time_stats']['total_time_spent']
    Estimated=i['time_stats']['time_estimate']
    creator = i['author']['name']
    
    try:
        assignee = i['assignee']['name']
    except:
        assignee = ''
    iid = i['iid']
    labels = i['labels']
    
    if closed_at is None :
        is_open = True
    else:   
        is_open = False
    
    
    # NOTES_URL=' '
    r = requests.get(NOTES_URL, headers=HEADER)
    i['notes'] = json.loads(r.text)

    notes_count = len(i['notes'])

    # Print out a record for the initial issue
    r = [title,datestr(created_at),datestr(updated_at),datestr(closed_at),str(Spent/60/60),str(Estimated/60/60),str(notes_count),str(iid),datestr(created_at),'',creator,assignee,'0','0','False',
        str('BUG' in labels), str('Support or Maintenance' in labels), str('Knowledge Transfer' in labels), str('High Priority' in labels), str('Medium Priority' in labels), str('Low Priority' in labels), 
        str('Enhancement' in labels),str('In Progress' in labels),str('Ready for Review' in labels),str(is_open)]
    ws.append(r)
    print('|'.join(r))
    #print(title + '|' + datestr(created_at) + '|' + datestr(updated_at) + '|' + datestr(closed_at) + '|' + str(total_time) + '|' + str(notes_count) + '|' + str(iid) + '|' + datestr(created_at) + '||' + creator + '|' + assignee + '|0|0')

    last_date = created_at
    last_person = creator
    for n in i['notes']:
        note_created = to_date(n['created_at'])
        note_person = n['author']['name']
        note_id = n['id']
        lapse = round(((note_created - last_date).total_seconds()/60/60),1)
        bizlapse = round(businesshours(last_date, note_created),1)

        # Print out a record for each issue comment
        r = [title,datestr(created_at),datestr(updated_at),datestr(closed_at),str(Spent/60/60),str(Estimated/60/60),str(notes_count),str(note_id),datestr(note_created),datestr(last_date),note_person,'N/A',str(lapse),str(bizlapse),str(not(last_person == note_person)),
            str('BUG' in labels), str('Support or Maintenance' in labels), str('Knowledge Transfer' in labels), str('High Priority' in labels), str('Medium Priority' in labels), str('Low Priority' in labels),
            str('Enhancement' in labels),str('In Progress' in labels),str('Ready for Review' in labels),str(is_open)]
        ws.append(r)
        #print(title + '|' + datestr(created_at) + '|' + datestr(updated_at) + '|'+ datestr(closed_at) + '|' + str(total_time) + '|' + str(notes_count) + '|' + str(note_id) + '|' + datestr(note_created) + '|' + datestr(last_date) + '|' + note_person + '|N/A|' + str(lapse) + '|' + str(bizlapse))
        print('|'.join(r))
        last_date = note_created
        last_person = note_person
		

wb.save('issue_out.xlsx')

with open('issues.json', 'w') as output:
  json.dump(issues,output,indent=4)

#---------------------------------------------------------------------------------------

import pandas as pd
data_xls = pd.read_excel('issue_out.xlsx', 'Sheet', index_col=None)
data_xls.to_csv('issue_out.csv', encoding='utf-8', index=False)

#curl --header "PRIVATE-TOKEN: ${GITLAB_IssuesExport}" URL