# Post Twitter status

import tweepy as tw
import os

def get_twitter_key(file_name):
	file = open(file_name, "r")
	consumer_key = file.readline()			# API key
	consumer_secret = file.readline()		# API key secret	
	access_token = file.readline()			# access token
	access_token_secret = file.readline()	# access token secret
	file.close() 
	return consumer_key.rstrip("\n"), consumer_secret.rstrip("\n"), access_token.rstrip("\n"), access_token_secret.rstrip("\n")
	

def get_api(consumer_key, consumer_secret, access_token, access_token_secret):
	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tw.API(auth, wait_on_rate_limit = True)
	return api

def start_thread(api, latest_update, total_doses_administered, total_doses_delivered, doses_administered_today):
	message = "THREAD VACCINAZIONI ITALIA AGGIORNATO AL " + latest_update + "\n"\
			  +"Totale dosi somministrate: " + total_doses_administered + "\n"\
			  +"Totale dosi consegnate: " + total_doses_delivered + "\n"\
			  +"Dosi somministrate oggi (" + latest_update + "): " + doses_administered_today + "\n"\
			  +"https://github.com/MatteoOrlandini/COVID-19-Vaccination-Italy\n"\
			  +"#vaccinoCovid\n"\
			  +"#vaccino\n"\
			  +"#COVID19\n"\
			  +"#vaccinareh24\n"\
			  +"#vaccinoAntiCovid\n"\
			  +"1/n"
	file_names = os.scandir("./Charts/" + latest_update)
	media_ids = []
	for file_name in file_names:
		res = api.media_upload(file_name)
		media_ids.append(res.media_id)
		if (len(media_ids) == 4):
			original_tweet = api.update_status(status = message, media_ids = media_ids)
	return(original_tweet)

def update_thread(api, latest_update, reply_tweet):
	file_names = os.scandir("./Charts/" + latest_update)
	media_ids = []
	j = 0
	number_of_reply = 1
	for file_name in file_names:
		res = api.media_upload(file_name)
		media_ids.append(res.media_id)
		if (len(media_ids) == 4):
			if (number_of_reply > 1):
				reply_tweet = api.update_status(status = str(number_of_reply)+"/n", \
								  media_ids = media_ids, \
								  in_reply_to_status_id = reply_tweet.id, \
								  auto_populate_reply_metadata = True)
			number_of_reply += 1			
			media_ids = []
			
	if (len(media_ids) > 1):
				reply_tweet = api.update_status(status = str(number_of_reply)+"/n", \
								  media_ids = media_ids, \
								  in_reply_to_status_id = reply_tweet.id, \
								  auto_populate_reply_metadata = True)
	return number_of_reply
								  
def	get_tweet_link(api, id, number_of_reply):
	tweets = api.user_timeline(id = id)
	id = tweets[number_of_reply - 1].id
	return "https://twitter.com/i/web/status/"+str(id)
	  
def post_tweet(twitter_key_file_name, latest_update, total_doses_administered, total_doses_delivered, doses_administered_today):
	consumer_key, consumer_secret, access_token, access_token_secret = get_twitter_key(twitter_key_file_name)
	
	api = get_api(consumer_key, consumer_secret, access_token, access_token_secret)
				  
	tweet = start_thread(api, latest_update, str(total_doses_administered), str(total_doses_delivered), str(doses_administered_today))
	
	number_of_reply = update_thread(api, latest_update, tweet)
	
	return get_tweet_link(api, "VacciniCovidITA", number_of_reply)