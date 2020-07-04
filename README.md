# Smilebot

_Serving smiles since 2020 💛_

## What

Not enough people know that you can shop on smile.amazon.com instead of amazon.com, you pay the same, and 0.5% of your order goes to a charity of your choice.

This is a twitter bot which, if mentioned, will identify amazon links in the mention (and then in the tweet that the mention was a reply to) and reply with smile links 🙂

The bot is written in Python (about 300 lines), authenticated with Twitter app-auth, and deployed on Heroku.

This code is bad (and I feel bad) so please feel free to contribute!

## Usage 

* Python modules and version used are in requirements.txt and runtime.txt
* set .env file with your twitter app creds (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) and LOG_LEVEL
* Run locally: `heroku local worker`

## Deploy

`Procfile` tells heroku what to run.

**!!! Copy the last mention ID that was processed into `oldest_mention_id.txt` !!!**

(need to fix this)

Then:

```
git push heroku master
```

Then don't forget to scale up the dyno:

```
heroku ps:scale worker=1
```

## Debug

Get logs

```
heroku logs --tail
```
