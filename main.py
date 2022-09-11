from datetime import date, timedelta
import google_calendar.event_funcs as event_funcs
import google_calendar.google_service as google_service
import parse.parser as parser


def main():
    # 1 request to INMO to get schedule
    # 2 create events
    # 2 #1 check if created

    # 0
    service = google_service.get_service()
    group = 'M3136'

    # 1
    # start of week
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    week = parser.get_schedule(group)

    for day in week.days:
        cur_date = str(start_of_week + timedelta(days=day.day_index))
        for lesson in day.lessons:
            start = cur_date + 'T' + lesson.time_start + ':00+03:00'

            end = cur_date + 'T' + lesson.time_end + ':00+03:00'

            event = {
                'summary': lesson.lesson,
                'location': lesson.address,
                'description': lesson.room,
                'start': {
                    'dateTime': start,  # '2022-09-11T12:00:00+03:00',
                },
                'end': {
                    'dateTime': end,  # '2022-09-11T14:00:00+03:00',
                },
                'colorId': lesson.type + 1,  # colors goes from 1 to 12
            }
            event_funcs.create_event(service, event)

    # event_funcs.create_event(service, event1)
    # event_funcs.create_event(service, event2)

    start = '2022-09-11T11:00:00+03:00'
    end = '2022-09-11T18:00:00+03:00'

    events = event_funcs.get_events_by_time(service, start, end)
    for event in events:
        event_funcs.delete_event(service, event['id'])

    # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                       maxResults=10, singleEvents=True,
    #                                       orderBy='startTime').execute()
    # events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    #     return

    # # Prints the start and name of the next 10 events
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])


if __name__ == '__main__':
    main()
