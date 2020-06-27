#!/usr/bin/env python

import os
import oauth2 as oauth
from requests_oauthlib import OAuth1Session
import json

def load_env(): 
  from dotenv import load_dotenv
  load_dotenv()

def get_api_client():
  consumer = oauth.Consumer(key=os.getenv("CONSUMER_KEY"), secret=os.getenv("CONSUMER_SECRET"))
  access_token = oauth.Token(key=os.getenv("ACCESS_TOKEN"), secret=os.getenv("ACCESS_TOKEN_SECRET"))
  client = oauth.Client(consumer, access_token)
  print(client)
  return client

def get_api_client2():
  oauth = OAuth1Session(os.getenv("CONSUMER_KEY"),
                       client_secret=os.getenv("CONSUMER_SECRET"),
                       resource_owner_key=os.getenv("ACCESS_TOKEN"),
                       resource_owner_secret=os.getenv("ACCESS_TOKEN_SECRET"))
  return oauth

def get_mentions(client, last_mention_id):
  # https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-mentions_timeline
  # mentions_endpoint = ""
  # params  = '?trim_user=1,since_id=' + str(last_mention_id)
  # mentions_endpoint += params

  #TODO Error handling on request
  # response, data = client.request(mentions_endpoint)

  params = {"trim_user": "1", "since_id" : str(last_mention_id)}

  response = client.get("https://api.twitter.com/1.1/statuses/mentions_timeline.json", params = params)

  print('MENTIONS RESPONSE')
  print (response.text)

  return response

def get_tweet(client, id):

  # statuses_endpoint = "https://api.twitter.com/labs/2/tweets/1276992893970833408"
  # params =  str(id) + '&tweet.fields=text,created_at,attachments,entities'
  # statuses_endpoint += params

  # statuses_endpoint = "https://api.twitter.com/labs/2/tweets.json?"
  # params =  'ids=' + str(id) + '&tweet.fields=text,created_at,attachments,entities'
  # statuses_endpoint += params
  
  params = {"ids": "1276881317557415937", "tweet.fields": "text,created_at,attachments,entities", "media.fields": "url", "expansions": "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id"}

  response = client.get("https://api.twitter.com/labs/2/tweets", params = params)

  print(response.text)

  # print(statuses_endpoint)

  #TODO error handling
  # response, data = client.request(statuses_endpoint)

  # print(data)
  # return json.loads(data)

def main():
  load_env()
  client = get_api_client2()

  t = get_tweet(client, 1276992893970833408)

  print (t)

  # TODO: Save the last m?ention ID in file
  mentions = get_mentions(client,1)

  # for mention in mentions:
    # print("dealing with mention " + mention['id_str'])
    # print(mention)
    
  #   reply_id = mention['in_reply_to_status_id']

  #   if(reply_id):
  #     get_tweet(client, reply_id)

if __name__ == "__main__":
    main()
