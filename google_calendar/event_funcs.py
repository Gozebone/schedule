import datetime


def create_event(service, event):
    # event = {
    #     'summary': 'ITMO schedule',
    #     'location': 'ITMO university',
    #     'description': 'Test event created from ITMO schedule',
    #     'start': {
    #         'dateTime': '2022-09-11T12:00:00+03:00',
    #     },
    #     'end': {
    #         'dateTime': '2022-09-11T14:00:00+03:00',
    #     },
    #     'recurrence': [
    #         'RRULE:FREQ=DAILY;COUNT=2'
    #     ],
    #     'attendees': [
    #         {'email': 'lpage@example.com'},
    #         {'email': 'sbrin@example.com'},
    #     ],
    #     'reminders': {
    #         'useDefault': False,
    #         'overrides': [
    #             {'method': 'popup', 'minutes': 228},
    #         ],
    #     },
    # }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

    # created_event = service.events().quickAdd(
    #     calendarId='primary',
    #     text='Appointment at Somewhere on June 3rd 10am-10:25am').execute()


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
