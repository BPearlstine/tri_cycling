from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def getCreds():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def toJson(icsObject):
    newEvent = False
    eventJson = {}
    eventList = []
    for line in icsObject:
        if newEvent:
            if line[:line.index(':')] == "SUMMARY":
                eventJson['summary'] = line[line.index(':'):]
            elif line[:line.index(':')] == "LOCATION":
                eventJson['location'] = line[line.index(':'):]
            elif line[:line.index(':')] == "DTSTART":
                eventJson['start'] = {
                    #TODO: convert line to correct datetime
                    'dateTime': line[line.index(':'):]
                }
            elif line[:line.index(':')] == "DTEND":
                eventJson['end'] = {
                    #TODO: convert line to correct datetime
                    'dateTime': line[line.index(':'):]
                }
            elif line[:line.index(':')] == "UID":
                eventJson['iCalUID'] = line[line.index(':'):]
            elif line[:line.index(':')] == "DESCRIPTION":
                eventJson['description'] = line[line.index(':'):]
            elif line[:line.index(':')] == "URL":
                eventJson['source'] = {'url': line[line.index(':'):]
                                       }
            elif line[:line.index(':')] == "RRULE":
                eventJson['recurrence'] = [rule for rule in line[line.index(':'):].split(';')]
        elif line == "BEGIN:VEVENT":
            newEvent = True
        elif line == "END:VEVENT":
            eventList.append(eventJson)
            eventJson = []
            newEvent = False
    return eventList

def callMeetup(url):
    calendar = ''
    return calendar

def main():
    urlList = [
        'https://www.meetup.com/torc-nc/events/ical/',
        'https://www.meetup.com/Tarwheels/events/ical/',
        'https://www.meetup.com/ondraft/events/ical/'
    ]
    creds = getCreds()
    toUpload = []
    for calendar in calendarList:
        toUpload.append(toJson(calendar))

    try:
        service = build('calendar', 'v3', credentials=creds)

        for event in calendarList:
            service.events().import_(calendarId='cb2ajgfjpk6bf9gifg6kg2hn1s@group.calendar.google.com', body=event).execute()


    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    main()