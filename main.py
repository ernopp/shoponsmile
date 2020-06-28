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

  # print(json.loads(response.content))

  return json.loads(response.content)

def send_tweet(client, text, in_reply_to_status_id):

  send_tweet_endpoint = "https://api.twitter.com/1.1/statuses/update.json"
  params = {"status": text, "in_reply_to_status_id": in_reply_to_status_id}

  response = client.post(send_tweet_endpoint, params = params)

  # print(response.content)
  return json.loads(response.content)

def smilify_url(url):
    # print('aiming to transform url ' + url )

    # https://regex101.com/
    regex = r"(https?:\/\/(.+?\.)?amazon\.com(\/[A-Za-z0-9\-\._~:\/\?#\[\]@!$&'\(\)\*\+,;\=]*)?)"
    matches = re.match(regex, url)

    if(matches):
      smilified_url = url.replace('www.amazon', 'smile.amazon', 1)
      return {"success": True, "smilified_url": smilified_url}
    else:
      smilified_url = ''
      return {"success": False, "smilified_url": smilified_url}

def reply_to_mention(client, mention_id, username, smilified_urls):

    if(len(smilified_urls) == 0):
      text = "@" + username + " couldn't find an amazon link above... so here's smile.amazon.com"
    elif(len(smilified_urls) == 1):
      text = "@" + username + " here's your link " + smilified_urls[0]
    else:
      text = "@" + username + " here are your links: "
      for s_url in smilified_urls:
        text += s_url + ', '
      text = text[:-2]  

    print('------- Replying - smilified_urls is '+ str(smilified_urls))
    print('------- Replying with tweet text: '+ text + '\n')

    response = send_tweet(client, text, mention_id)

    if("errors" in response):
      print('------- Completed with error: ')
      print(response)
    else:
      print('------- Completed successfully, reply tweet id is: ' + str(response["id"]))

def get_amzn_urls_from_tweet(tweet):

  amzn_urls = []

  if("entities" in tweet['data'][0]):  
    if("urls" in tweet['data'][0]["entities"]):

      urls = tweet['data'][0]['entities']['urls'] 
      for url in urls:
          if(not "unwound_url" in url):
            break

          print("-------------- unwound url is " + url['unwound_url'])
          amzn_urls.append(url['unwound_url'])

  return amzn_urls

def get_smilified_urls_from_amzn_urls(amzn_urls):

  smilified_urls = []
  
  for u in amzn_urls:
    smilified_url = smilify_url(u)
    if(smilified_url['success']):
      smilified_urls.append(smilified_url['smilified_url'])
      print('----------------------------new smile url is ' + smilified_url['smilified_url'])

  return smilified_urls

def main():

  # TODO: Save the last mention ID in file
  mentions = get_mentions(client,1)

  for mention in mentions:
    mention_id = mention['id_str']
    
    # Have to do this to get the labs v2 version of the tweet with unwound urls
    mention_tweet = get_tweet(client, mention_id)

    print("\n\n---- PROCESSING MENTION ID: " + mention_id )

    username =  mention['user']['screen_name']
    print("------- username that wrote mention is : " + username )

    print("------- mention text: " + mention['text'])

    smilified_urls = []
    
    original_tweet_id = mention['in_reply_to_status_id_str']
    
    if(original_tweet_id):
    
      #MENTION IS IN REPLY TO A TWEET
    
      print("------- mention is reply to original tweet id:  " + original_tweet_id)

      original_tweet = get_tweet(client, original_tweet_id)

      print("------- original tweet text is:  " + original_tweet["data"][0]["text"])

      # GET AMAZON TWEETS FROM ORIGINAL TWEET
      original_tweet_amzn_urls = get_amzn_urls_from_tweet(original_tweet)
      print("------- found " + str(len(original_tweet_amzn_urls)) + " amzn links in original tweet")
      smilified_urls += get_smilified_urls_from_amzn_urls(original_tweet_amzn_urls)
           
    else:
      print('-------mention was not a reply to a tweet')

      mention_amzn_urls = get_amzn_urls_from_tweet(mention_tweet)
      print("------- found " + str(len(mention_amzn_urls)) + " amzn links in mention tweet")
      smilified_urls += get_smilified_urls_from_amzn_urls(mention_amzn_urls)

    #dedupe
    smilified_urls = list( dict.fromkeys(smilified_urls) )
    
    reply_to_mention(client, mention_id, username, smilified_urls)

if __name__ == "__main__":
    load_env()
    client = get_api_client()
    main()

    # send_tweet(client,"@ernopp testingasdasd123 https://www.smile.amazon.com/dp/1442265639/ref=cm_sw_r_cp_api_i_ze19Eb5DRNN42", '1273945165217124352')

    # print(smilify_url('https://www.amazon.com/dp/1442265639/ref=cm_sw_r_cp_api_i_ze19Eb5DRNN42'))

    # t = get_tweet(client, '1276631955132407808')
    # print(t)