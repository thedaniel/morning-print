from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pytz
import iso8601
tz = pytz.timezone('Europe/Amsterdam')


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main(prefix=None):
  if prefix:
    prefix = f'{prefix}_'
  else:
    prefix = ''
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  token_path = f'{prefix}token.json'
  if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_path, 'w') as token:
      token.write(creds.to_json())

  service = build('calendar', 'v3', credentials=creds)

  # Call the Calendar API
  now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
  until_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
  until = until_dt.isoformat() + 'Z'
  events_result = service.events().list(
    calendarId='primary', 
    timeMin=now,
    timeMax=until,
    singleEvents=True,
    orderBy='startTime'
    ).execute()
  events = events_result.get('items', [])
  return events


if __name__ == '__main__':
  events = main()
  work_events = main(prefix="work")
  if not events:
    print('No personal events.')
  for event in events:
    # TODO: convert to the right time zone
    try:
      start = iso8601.parse_date(event['start'].get('dateTime')).astimezone(tz).strftime('%-H:%M')
    except:
      start = 'today'
    print(start, event['summary'])

  if not work_events:
    print('No work events.')
  for event in work_events:
    try:
      start = iso8601.parse_date(event['start'].get('dateTime')).astimezone(tz).strftime('%-H:%M')
    except:
      start = 'today'
    print(start, event['summary'])
