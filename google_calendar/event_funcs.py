import datetime


def create_event(service, event):
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def delete_event(service, id):
    service.events().delete(calendarId='primary',
                            eventId=id).execute()


def get_events(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])


def get_events_by_time(service, start, end):
    events_result = service.events().list(calendarId='primary', timeMin=start,
                                          timeMax=end, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])
