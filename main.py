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
  params = {"since_id" : str(last_mention_id)}

  #TODO error handling
  response = client.get(mentions_endpoint, params = params)

  return json.loads(response.content)

def get_tweet(client, id):

  statuses_endpoint = "https://api.twitter.com/labs/2/tweets"
  
  params = {"ids": id, "tweet.fields": "text,created_at,attachments,entities", "media.fields": "url", "expansions": "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id", "user.fields" : "username"}

  #TODO error handling
  response = client.get(statuses_endpoint, params = params)

  return json.loads(response.content)

def send_tweet(client, text, in_reply_to_status_id):
  send_tweet_endpoint = "https://api.twitter.com/1.1/statuses/update.json"
  params = {"status": text, "in_reply_to_status_id": in_reply_to_status_id}

  response = client.post(send_tweet_endpoint, params = params)

  print(response.content)
  # return json.loads(response.content)

def transform_amazon_url(url):
    print('aiming to transform url ' + url )

    # https://regex101.com/
    regex = r"(https?:\/\/(.+?\.)?amazon\.com(\/[A-Za-z0-9\-\._~:\/\?#\[\]@!$&'\(\)\*\+,;\=]*)?)"
    matches = re.match(regex, url)

    if(matches):
      transformed_url = url.replace('www.amazon', 'smile.amazon', 1)
      return {"success": True, "transformed_url": transformed_url}
    else:
      transformed_url = ''
      return {"success": False, "transformed_url": transformed_url}

def main():

  # TODO: Save the last mention ID in file
  mentions = get_mentions(client,1)

  for mention in mentions:
    mention_id = mention['id_str']
    print("---- PROCESSING MENTION ID: " + mention_id )
    username =  mention['user']['screen_name']
    print("------- username that wrote mention is : " + username )
    print("------- mention text" + mention['text'])
    
    original_tweet_id = mention['in_reply_to_status_id_str']
    
    if(original_tweet_id):
    
      #MENTION IS IN REPLY TO A TWEET
    
      print("-------------- found an original tweet id  " + original_tweet_id)

      replied_tweet = get_tweet(client, original_tweet_id)
      print("-------------- the original tweet is  ")
      print(replied_tweet)
      
      urls = replied_tweet['data'][0]['entities']['urls'] 
      #wrong username to reply to
      # username = replied_tweet['includes']['users'][0]['username']

      if (urls):  

        for url in urls:

          transformed_url = transform_amazon_url(url['unwound_url'])
          
          if(transformed_url['success']):
            print('----------------------------matched amazon url')
            print('----------------------------new smile url is ' + transformed_url['transformed_url'])
            # TODO send the smile tweet back 

            text = "Hey @" + username + " here is your smile link: " +  transformed_url['transformed_url']
            send_tweet(client, text, mention_id)

          else:
            print('--------------couldnt match amazon url in original tweet')
      
      else:
        print('--------------no amazon url found in original tweet')
        #TODO generic tweet

    else:
      print('-------mention was not a reply to a tweet')
      #TODO check if there is a url in the mention, if so transform it and return
      #TODO generic tweet

if __name__ == "__main__":
    load_env()
    client = get_api_client()
    main()

    # send_tweet(client,"@ernopp testingasdasd123 https://www.smile.amazon.com/dp/1442265639/ref=cm_sw_r_cp_api_i_ze19Eb5DRNN42", '1273945165217124352')

    # print(transform_amazon_url('https://www.amazon.com/dp/1442265639/ref=cm_sw_r_cp_api_i_ze19Eb5DRNN42'))

    # t = get_tweet(client, '1276631955132407808')
    # print(t)