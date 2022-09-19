from datetime import date, timedelta
import google_calendar.event_funcs as event_funcs
import google_calendar.google_service as google_service
import parse.parser as parser


def compare_events(cur_event, event):
    compare_keys = ['summary', 'location', 'description', 'colorId', 'start']
    for compare_key in compare_keys:
        if event[compare_key] == cur_event[compare_key]:
            break
        return False

    start_event = event['start'].get('dateTime', event['start'].get('date'))
    start_cur_event = cur_event['start'].get('dateTime', cur_event['start'].get('date'))
    if start_event != start_cur_event:
        return False

    return True


def compare_list_events(events, cur_event):
    for event in events:
        if compare_events(cur_event, event):
            return True
    return False


def main():
    service = google_service.get_service()
    group = input().capitalize()

    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    week = parser.get_schedule(group)

    for day in week.days:
        cur_date = str(start_of_week + timedelta(days=day.day_index))
        for lesson in day.lessons:
            start = cur_date + 'T' + lesson.time_start + ':00+03:00'

            end = cur_date + 'T' + lesson.time_end + ':00+03:00'

            cur_event = {
                'summary': lesson.lesson,
                'location': lesson.address,
                'description': lesson.room,
                'start': {
                    'dateTime': start,
                },
                'end': {
                    'dateTime': end,
                },
                'colorId': lesson.type + 1,  # colors goes from 1 to 12
            }

            events_result = service.events().list(calendarId='primary', timeMin=start,
                                                  timeMax=end, singleEvents=True).execute()
            events = events_result.get('items', [])

            if not compare_list_events(events, cur_event):
                event_funcs.create_event(service, cur_event)


if __name__ == '__main__':
    main()
