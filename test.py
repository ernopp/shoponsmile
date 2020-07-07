import json

empty = json.loads("[]")

singlejson = json.loads("[{\"a\": 1, \"b\": 123}]")

severaljsons = json.loads("[{\"a\": 1, \"b\": 123}, {\"a\": 2, \"b\": 234}]")

empty.reverse()
singlejson.reverse()
severaljsons.reverse()

print(empty)
print(singlejson)
print(severaljsons)


#  [{'screen_name': 'eriktorenberg', 'name': 'Erik Torenberg', 'id': 1475495658, 'id_str': '1475495658', 'indices': [0, 14]}, {'screen_name': 'ShopOnSmile', 'name': 'Shop on Smile', 'id': 12751
# 22:10:45 worker.1   |  >  06249047265292, 'id_str': '1275106249047265292', 'indices': [18, 30]}], 'urls': []}, 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'in_reply_to_status_id': 1280033612574801920, 'in_reply_to_status_id_str': '1280033612574801920', 'in_reply_to_user_id': 1475495658, 'in_reply_to_user_id_str': '1475495658', 'in_reply_to_screen_name': 'eriktorenberg', 'user': {'id': 254809616, 'id_str': '254809616', 'name': 'Ernest 
# Oppetit', 'screen_name': 'ErnOpp', '
# 22:10:45 worker.1   |  >  location': 'London', 'description': 'Product Manager at @Improbableio. Learning & questioning in public', 'url': 'https://t.co/qJ6dejOQgK', 'entities': {'url': {'urls': [{'url': 'https://t.co/qJ6dejOQgK', 'expanded_url': 'https://ernest.oppet.it/', 'display_url': 'ernest.oppet.it', 'indices': [0, 23]}]}, 'description': {'urls': []}}, 'protected': False, 'followers_count': 1370, 'friends_count': 3279, 'listed_count': 118, 'created_at': 'Sun Feb 20 02:02:36 +0000 2011', 'favourites_count': 11220,
# 22:10:45 worker.1   |  >  'utc_offset': None, 'time_zone': None, 'geo_enabled': True, 'verified': False, 'statuses_count': 3576, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': '04080A', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profi
# 22:10:45 worker.1   |  >  le_images/1241399994353160195/Bd4p3XCs_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1241399994353160195/Bd4p3XCs_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/254809616/1521418963', 'profile_link_color': 'A8001F', 'profile_sidebar_border_color': 'FFFFFF', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': True, 'default_profile': False, 'default_profile_
# 22:10:45 worker.1   |  >  image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 0, 'favorite_count': 0, 'favorited': False, 'retweeted': False, 'lang': 'und'}]