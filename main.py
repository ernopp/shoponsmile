#!/usr/bin/env python

import os
import sys
from requests_oauthlib import OAuth1Session
import json
import re
import random
import coloredlogs, logging
import time
from dotenv import load_dotenv # https://pypi.org/project/python-dotenv/

def get_api_client():

  oauth = OAuth1Session(os.getenv("CONSUMER_KEY"),
                       client_secret=os.getenv("CONSUMER_SECRET"),
                       resource_owner_key=os.getenv("ACCESS_TOKEN"),
                       resource_owner_secret=os.getenv("ACCESS_TOKEN_SECRET"))
  return oauth

def get_mentions(client, last_mention_id):

  mentions_endpoint = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'

  # since_id Returns results with an ID greater than (that is, more recent than) the specified ID
  params = {"since_id" : str(last_mention_id)}

  response = client.get(mentions_endpoint, params = params)

  logging.debug('mentions api call response ' + str(response))

  return json.loads(response.content)

def get_tweet(client, id):

  statuses_endpoint = "https://api.twitter.com/labs/2/tweets"
  
  params = {"ids": id, "tweet.fields": "text,created_at,attachments,entities", "media.fields": "url", "expansions": "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id", "user.fields" : "username"}

  response = client.get(statuses_endpoint, params = params)

  # logging.debug(json.loads(response.content))

  return json.loads(response.content)

def send_tweet(client, text, in_reply_to_status_id):

  send_tweet_endpoint = "https://api.twitter.com/1.1/statuses/update.json"
  params = {"status": text, "in_reply_to_status_id": in_reply_to_status_id}

  response = client.post(send_tweet_endpoint, params = params)
  # logging.debug(response.content)
  return json.loads(response.content)

def smilify_url(url):
    # logging.debug('aiming to transform url ' + url )

    # https://regex101.com/
    regex = r"(https?:\/\/(.+?\.)?amazon\.com(\/[A-Za-z0-9\-\._~:\/\?#\[\]@!$&'\(\)\*\+,;\=]*)?)"
    matches = re.match(regex, url)

    if(matches):
      smilified_url = url.replace('www.amazon', 'smile.amazon', 1)
      return {"success": True, "smilified_url": smilified_url}
    else:
      smilified_url = ''
      return {"success": False, "smilified_url": smilified_url}

def reply_to_mention(client, mention_id, username_who_mentioned, original_tweet_username, smilified_urls):

    zero_link_replies = ["Hmmm I couldn't find an Amazon link above...😳. So here's my homepage: smile.amazon.com. Shop from here and 0.5% of your order goes to a charity of your choice 💛"]
    one_link_replies = ["Yes, spot on. Here's your AmazonSmile link: shop with this one and 0.5% of your order goes to a charity of your choice (you pay the same) 💛 ", "AmazonSmile link FTW. Shop with this link and 0.5% of your order goes to a charity of your choice (you pay the same). Here ya go 💛 ", "I concur. You get a Smile link, you get a Smile link. Everyone gets a Smile link (through which 0.5% of your order goes to a charity of your choice) 💛", "What a time to be alive. Here's your AmazonSmile link. Shop with this one and 0.5% of your order goes to a charity of your choice (you pay the same) 💛 "]
    multi_link_replies = ["WOAH! Multi-link combo action. Here are your AmazonSmile links, friend. Shop with these and 0.5% of your order goes to a charity of your choice 💛 "]

    original_tweet_username_string = " "
    if(original_tweet_username is not None):
      original_tweet_username_string += "@" + str(original_tweet_username) + " "

    if(len(smilified_urls) == 0):
      text = "@" + username_who_mentioned + original_tweet_username_string + random.choice(zero_link_replies)
    elif(len(smilified_urls) == 1):
      text = "@" + username_who_mentioned + original_tweet_username_string + random.choice(one_link_replies) + smilified_urls[0]
    else:
      text = "@" + username_who_mentioned + original_tweet_username_string + random.choice(multi_link_replies)
      for s_url in smilified_urls:
        text += s_url + ', '
      text = text[:-2]  

    logging.debug('------- Replying - smilified_urls is '+ str(smilified_urls))
    logging.debug('------- Replying with tweet text: '+ text + '\n')

    response = send_tweet(client, text, mention_id)

    if("errors" in response):
      logging.error('------- Completed with error: ')
      logging.error(response)
    else:
      logging.info('------- Completed successfully, reply tweet id is: ' + str(response["id"]))

def get_amzn_urls_from_tweet(tweet):

  amzn_urls = []

  if("entities" in tweet['data'][0]):  
    if("urls" in tweet['data'][0]['entities']):

      urls = tweet['data'][0]['entities']['urls'] 
      for url in urls:
          if(not "unwound_url" in url):
            break

          logging.debug("-------------- unwound url is " + url['unwound_url'])
          amzn_urls.append(url['unwound_url'])

  return amzn_urls

def get_smilified_urls_from_amzn_urls(amzn_urls):

  smilified_urls = []
  
  for u in amzn_urls:
    smilified_url = smilify_url(u)
    if(smilified_url['success']):
      smilified_urls.append(smilified_url['smilified_url'])
      logging.debug('----------------------------new smile url is ' + smilified_url['smilified_url'])

  return smilified_urls

def get_oldest_mention_id_processed():

  try: 
    oldest_mention_id_processed = 1
    file = open('oldest_mention_id.txt', 'r+')
    oldest_mention_id_processed = file.read()
    file.close()
    return oldest_mention_id_processed

  except:
    logging.error("Unexpected error in get_oldest_mention_id_processed: " + sys.exc_info()[0]) 

def save_oldest_mention_id_processed(oldest_mention_id_processed):
  
  try: 
    # a+ opens if doesnt exist
    file = open('oldest_mention_id.txt', 'a+') 
    file.truncate(0)
    file.write(str(oldest_mention_id_processed))
    file.close()

  except:
    logging.error("Unexpected error in save_oldest_mention_id_processed: " + sys.exc_info()[0]) 

def main():

  try:
    # Get oldest mention id processed
    oldest_mention_id_processed = get_oldest_mention_id_processed()

    logging.info("oldest_mention_id_processed is " + str(oldest_mention_id_processed))

    mentions = get_mentions(client, oldest_mention_id_processed)

    logging.info("mentions is " + str(mentions))
    logging.info(mentions)

    if("errors" in mentions):  
      logging.error("exiting main with error in mentions")
      return

    # Mentions API returns most recent first. We want to process oldest first. 
    mentions.reverse()

    for mention in mentions:

      mention_id = mention["id_str"]
      oldest_mention_id_processed = mention_id
      original_tweet_username = None
      
      logging.info("\n\n---- PROCESSING MENTION ID: " + mention_id )
      
      logging.debug("\n\n---- CREATED AT : " + mention["created_at"] )

      if(mention["in_reply_to_user_id_str"]=="1275106249047265292"):
        logging.debug("------- Mention is to self... SKIPPING")  
        continue

      # Have to do this to get the labs v2 version of the tweet with unwound urls
      mention_tweet = get_tweet(client, mention_id)

      username_who_mentioned =  mention['user']['screen_name']
      logging.debug("------- username that wrote mention is : " + username_who_mentioned )

      logging.debug("------- mention text: " + mention['text'])

      smilified_urls = []
      
      original_tweet_id = mention['in_reply_to_status_id_str']
      
      if(original_tweet_id):
      
        #MENTION IS IN REPLY TO A TWEET

        original_tweet_username = mention['in_reply_to_screen_name']
      
        logging.debug("------- mention is reply to original tweet id:  " + original_tweet_id)

        original_tweet = get_tweet(client, original_tweet_id)

        if("errors" in original_tweet):
          logging.info("error retrieving original tweet. Maybe no access. Skipping mention ")
          continue

        logging.debug("------- original tweet text is:  " + str(original_tweet))
        # logging.debug("------- original tweet text is:  " + original_tweet['data'][0]['text'])

        # GET AMAZON TWEETS FROM ORIGINAL TWEET
        original_tweet_amzn_urls = get_amzn_urls_from_tweet(original_tweet)
        logging.debug("------- found " + str(len(original_tweet_amzn_urls)) + " amzn links in original tweet")
        smilified_urls += get_smilified_urls_from_amzn_urls(original_tweet_amzn_urls)
            
      else:
        logging.debug('-------mention was not a reply to a tweet')

        mention_amzn_urls = get_amzn_urls_from_tweet(mention_tweet)
        logging.debug("------- found " + str(len(mention_amzn_urls)) + " amzn links in mention tweet")
        smilified_urls += get_smilified_urls_from_amzn_urls(mention_amzn_urls)

      #dedupe
      smilified_urls = list( dict.fromkeys(smilified_urls) )
      
      # client, mention_id, username_who_mentioned, original_tweet_username, smilified_urls
      
      reply_to_mention(client, mention_id, username_who_mentioned, original_tweet_username, smilified_urls)

    logging.info("\n\n Saving oldest_mention_id_processed " + oldest_mention_id_processed)
    save_oldest_mention_id_processed(oldest_mention_id_processed)

  except Exception as e:
    logging.error(e, exc_info=True)

# def test_exceptions():
#   test= {"asd", 123}

#   try:
#     print(test["1414"])
#   except Exception as e:
#   #   print("error")
#   #   traceback.print_exc()
#     logging.error(e, exc_info=True)

#     # logging.error('Caught an error' , sys.exc_info()[0])

if __name__ == "__main__":
    load_dotenv()
    
    coloredlogs.install(level=os.getenv("LOG_LEVEL"))
    logging.info("log level is " + str(os.getenv("LOG_LEVEL")))

    client = get_api_client()
    
    starttime = time.time()

    # RUN WHEN TRIGGERED
    # main()

    # SLEEP 20 SECONDS AFTER EACH RUN
    
    while True:
      logging.info("tick")
      main()
      time.sleep(20.0)
      # Mentions API rate limit: 75 requests / 15-minutes

    # send_tweet(client,"@ernopp testingasdasd123 https://www.smile.amazon.com/dp/1442265639/ref=cm_sw_r_cp_api_i_ze19Eb5DRNN42", '1273945165217124352')

    # logging.debug(smilify_url('https://www.amazon.com/dp/1442265639/ref=cm_sw_r_cp_api_i_ze19Eb5DRNN42'))

    # t = get_tweet(client, '1276631955132407808')
    # logging.debug(t)

