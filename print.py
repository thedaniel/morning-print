from escpos.printer import Usb, Dummy
import requests
from time import sleep
from dotenv import dotenv_values
from random import choice
from gcal import main as cal
config = dotenv_values(".env")

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
  print(book)
  return quote


# ids = [] # will mark these as seen in the db but this is just for dev

# while True:
#    r = requests.post('https://thermalist.herokuapp.com/pop')
#    messages = r.json()
#    print(messages)
#    for m in messages:
#       if m['id'] not in ids:
#          p.text(f'{m["message"]}\n')

#    ids += [m['id'] for m in messages]
#    sleep(10)

def _print():
  quote = readwise()
  events = cal()
  p.ln()
  p.textln(quote['text'])
  p.textln(f" - {quote['book']['title']}, by {quote['book']['author']}")
  p.ln()
  p.textln("Events")
  p.ln()
  if not events:
    p.textln('No upcoming events found.')
  for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    p.textln(f"{start}  {event['summary']}")
    p.ln()
  p.ln(count=3)

if __name__ == '__main__':
  _print()