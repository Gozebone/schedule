from calendar import calendar
import datetime

CALENDAR_NAME = "ITMO Schedule"


def create_calendar(service):
    calendar = {
        'summary': CALENDAR_NAME,
        'timeZone': 'Europe/Moscow'
    }

    service.calendars().insert(body=calendar).execute()


def is_schedule_calendar_exist(service):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == CALENDAR_NAME:
                return True
            
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
        
    return False
        
        

def get_schedule_calendar(service):
    page_token = None
    schedule_calendar = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == CALENDAR_NAME:
                schedule_calendar = calendar_list_entry
                break
            
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    if schedule_calendar == None:
        print(f"No {CALENDAR_NAME} calendar found\nCheck if you have renamed it")
        
    return schedule_calendar


def create_event(service, calendar, event):
    event = service.events().insert(calendarId=calendar['id'], body=event).execute()
    print('Event created in calendar: %s \nLink: %s' % (calendar['summary'], event.get('htmlLink')))


# Example call: 
#event_funcs.delete_event(service, event['id']) 
def delete_event(service, id):
    service.events().delete(calendarId='primary',
                            eventId=id).execute()


def get_events(service, amount: int):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=amount, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])


def get_events_by_time(service, start, end):
    events_result = service.events().list(calendarId='primary', timeMin=start,
                                          timeMax=end, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])
