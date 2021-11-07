from escpos.printer import Usb, Dummy
import requests
from time import sleep
from dotenv import dotenv_values
from random import choice
from gcal import main as cal
import pytz
import iso8601
import sys

config = dotenv_values(".env")
tz = pytz.timezone('Europe/Amsterdam')

p = Usb(0x28e9, 0x0289)
# p = Dummy

def readwise():
  results = []
  querystring = {
    "page_size": 1000,
  }

  response = requests.get(
     url="https://readwise.io/api/v2/highlights/",
     headers={"Authorization": f'Token {config["READWISE_TOKEN"]}'},
     params=querystring
  )

  data = response.json()
  results.extend(data['results'])
  # TODO paginate
  quote = choice(results)
  book = requests.get(
     url=f"https://readwise.io/api/v2/books/{quote['book_id']}",
     headers={"Authorization": f'Token {config["READWISE_TOKEN"]}'},
  )
  book = book.json()
  quote['book'] = book
  return quote

def _print():
  quote = readwise()
  try:
    events = cal()
  except Exception as e:
    print('Error getting PERSONAL calendar events. You probably need to re-auth. rm token.json && python gcal.py')
    print(e)
    sys.exit(1)
  try:
    work_events = cal(prefix='work')
  except Exception as e:
    print('Error getting WORK calendar events. You probably need to re-auth.\nrm work_token.json here and python gcal.py on your work computer and copy token.json to work_token.json')
    print(e)
    sys.exit(1)

  p.ln()
  p.textln(quote['text'])
  p.textln(f" - {quote['book']['title']}, by {quote['book']['author']}")
  p.ln()
  p.textln("Events")
  p.ln()
  p.textln('Personal events')
  p.textln('---------------')
  for event in events:
    try:
      start = iso8601.parse_date(event['start'].get('dateTime')).astimezone(tz).strftime('%-H:%M')
    except:
      start = 'today'
    p.textln(f"{start}  {event.get('summary', '')}")
    p.ln()
  p.ln()
  p.textln('Work events')
  p.textln('---------------')
  for event in work_events:
    try:
      start = iso8601.parse_date(event['start'].get('dateTime')).astimezone(tz).strftime('%-H:%M')
    except:
      start = 'today'
    p.textln(f"{start}  {event.get('summary', '')}")
    p.ln()
  p.ln(count=3)

if __name__ == '__main__':
  _print()