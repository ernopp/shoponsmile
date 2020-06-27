#!/usr/bin/env python

import os
from requests_oauthlib import OAuth1Session
import json
import re

def load_env(): 
  from dotenv import load_dotenv
  load_dotenv()

def get_api_client():

  oauth = OAuth1Session(os.getenv("CONSUMER_KEY"),
                       client_secret=os.getenv("CONSUMER_SECRET"),
                       resource_owner_key=os.getenv("ACCESS_TOKEN"),
                       resource_owner_secret=os.getenv("ACCESS_TOKEN_SECRET"))
  return oauth

def get_mentions(client, last_mention_id):

  mentions_endpoint = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
  params = {"trim_user": "1", "since_id" : str(last_mention_id)}

  #TODO error handling
  response = client.get(mentions_endpoint, params = params)

  return json.loads(response.content)

def get_tweet(client, id):

  statuses_endpoint = "https://api.twitter.com/labs/2/tweets"
  
  params = {"ids": "1276881317557415937", "tweet.fields": "text,created_at,attachments,entities", "media.fields": "url", "expansions": "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id"}

  #TODO error handling
  response = client.get(statuses_endpoint, params = params)

  return json.loads(response.content)

def transform_amazon_url(url):
    print('aiming to transform url ' + url )

    # https://regex101.com/
    regex = r"(https?:\/\/(.+?\.)?amazon\.com(\/[A-Za-z0-9\-\._~:\/\?#\[\]@!$&'\(\)\*\+,;\=]*)?)"
    matches = re.match(regex, url)

    if(matches):
      transformed_url = url.replace('amazon', 'smile.amazon', 1)
      return {"success": True, "transformed_url": transformed_url}
    else:
      transformed_url = ''
      return {"success": False, "transformed_url": transformed_url}

def main():
  load_env()
  client = get_api_client()

  # TODO: Save the last mention ID in file
  mentions = get_mentions(client,1)

  for mention in mentions:
    print("---- Mention is ID: " + mention['id_str'])
    print(mention)
    
    reply_id = mention['in_reply_to_status_id_str']
    
    if(reply_id):
    
      #MENTION IS IN REPLY TO A TWEET
    
      print("--------- found a reply ID " + reply_id)

      replied_tweet = get_tweet(client, reply_id)
      print("--------------- replied to tweet is  ")
      print(replied_tweet)
      
      urls = replied_tweet['data'][0]['entities']['urls'] 

      if (urls):  

        for url in urls:

          transformed_url = transform_amazon_url(url['unwound_url'])
          
          if(transformed_url['success']):
            print('matched amazon url')
            print('new smile url is ' + transformed_url['transformed_url'])
            # TODO send the smile tweet back 

          else:
            print('couldnt match amazon url in this tweet')
      
      else:
        print('no amazon url found in tweet')
        #TODO generic tweet

    else:
      print('mention without a reply')
      #TODO generic tweet

if __name__ == "__main__":
    main()
    # print(transform_amazon_url('https://www.amazon.com/dp/1442265639/ref=cm_sw_r_cp_api_i_ze19Eb5DRNN42'))
