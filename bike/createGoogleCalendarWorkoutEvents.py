#!/usr/bin/env python3

import sys
import argparse
import datetime

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.contrib.dictionary_storage import DictionaryStorage

def main():
    if sys.version_info.major < 3:
        print('Python 3+ required')
        return

    tools.argparser.add_argument('year', type=int, help='The year of the first event')
    tools.argparser.add_argument('month', type=int, help='The month of the first event')
    tools.argparser.add_argument('day', type=int, help='The day of the first event')
    flags = tools.argparser.parse_args()

    eventDay = datetime.date(flags.year, flags.month, flags.day)
    userResponse = input('Is date {} correct? y/n: '.format(eventDay.strftime('%A, %B %d, %Y')))
    if userResponse.lower() != 'y':
        return

    storage_dict = {}
    store = DictionaryStorage(storage_dict, u'credentials')
    flow = client.OAuth2WebServerFlow(
        client_id='570017343303-nf4f1vaclctc8d0c7ma4rahm5v49rnbm.apps.googleusercontent.com',
        client_secret='BDhRKaNZh4iRRfr2V95y3y2O',
        scope='https://www.googleapis.com/auth/calendar',
        auth_uri='https://accounts.google.com/o/oauth2/auth',
        token_uri='https://www.googleapis.com/oauth2/v3/token')
    creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    oneDay = datetime.timedelta(days=1)
    for week in range(1, 5):
        for day in range(1, 8):
            event = {
                'summary': 'W{}D{}'.format(week, day),
                'transparency': 'transparent',
                'start': {
                    'date': str(eventDay),
                },
                'end': {
                    'date': str(eventDay),
                },
            }
            eventDay += oneDay
            event = service.events().insert(calendarId='primary', body=event).execute()

    print('')
    print('Events created')

if __name__ == '__main__':
    main()