# Morning Print

Prints some calendar items and a random quote from readwise.io. Code is ugly and
full of copy paste and hardcoding at the moment, it's just a quick personal utility.

## Gcal tokens

The gcal stuff is adapted from a google cal api quickstart that i don't have the
ink to handy, you'll need to:

- create an app and some credentials for it and save them in the root dir as
  `credentials.json`
  - if the app is in testing mode you'll have to add the emails you want to use
    as testers
- Create a python3 venv, activate it, `pip install -r requirements.txt`
- `python gcal.py` will open your browser to do the oauth dance and save token,
  and print events to stdout if it worked.
  - Right now I have it hardcoded to use `token.json` and `work_token.json`,
    basically i just checked this out on my work computer and ran it there and
    copied the `token.json` to the printer computer and renamed it to
    `work_token.json`
    
## Readwise

`.env` file with `READWISE_TOKEN=<token>` should be all that's necessary

## Run it

`python print.py`

## Hardware

I have a [GOOJPRT
PT-210](https://www.aliexpress.com/wholesale?catId=0&initiative_id=AS_20210607075245&origin=y&SearchText=goojprt+pt210)
- also available on amazon and other sites. Most generic thermal printers should
  work

## TODO

- If the token expires the script crashes, it should probably just re-auth if it
  can
- maybe print error messages to the printer instead of showing them on stdout?
- paginate readwise
- filter out "readwise team" higlights