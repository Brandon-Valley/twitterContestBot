# big thanks to Robbie Barrat for writing some helpful code and github user 'timster' for optimizing a lot of rough bits
import tweepy
import time

#stuff to do:
#make it stop following bot spotters
#make it follow any other user mentioned in a tweet
#fix misc errors
#play with timer speed
#add ability to tag friends
#split stuff up for multiple bot usage
#maybe add something so even if you rt a new contest, if you are already follow them, dont follow again - is this a real problem???
#once it can run for a day - make it write the time/other data to exel sheet and set it up to graph stuff like rt's per hour to see most active times each day


#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'UeP2AalTDFKHPyLav70Lmi1Zx' #keep the quotes, enter your consumer key
CONSUMER_SECRET = '9zwnGkYGVfieUIxJfc6i55vWd3WegFMlSKmK8AsCcpNLI0d3Rw'#keep the quotes, enter your consumer secret key
ACCESS_KEY = '885340635854753793-5XDrIQmk1mnoOoslMnnx01k6I74nxOD'#keep the quotes, enter your access token
ACCESS_SECRET =  'AqB2R8jCRs9us7cXzIc7jJp8yZYM7ALJxU1XslFDT14OR'#keep the quotes, enter your access token secret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

rtKeywords = ["rt to", "rt and win", "retweet and win",
              "rt for", "rt 4", "retweet to"]

followKeywords = ['follow', 'Follow', 'FOLLOW']

favKeywords = ['fav', 'Fav', 'FAV']

bannedwords = ["vote"]


def search(twts):
    for i in twts:
        if not any(k in i.text.lower() for k in rtKeywords) or any(k in i.text.lower() for k in bannedwords):
            continue
        # Retweets
        try:
            api.retweet(i.id)
            print ("JUST RETWEETED " + (i.text))
            print('TEST- i.text:', i.text)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            print('TEST- i.text.lower():', i.text.lower())#!!!!!!!!!!!!!!!!!!!!!!!!!
        except:
            print ("Hm... Something went wrong. - probably already retweeted this.")
        # Follows
        if any(k in i.text for k in followKeywords):
            # This part follows the actual contest-holder, instead of some random person who retweeted their contest
            tweet = i.text
            if tweet[0:3] == "RT ":
                tweet = tweet[3:]
            if tweet[0] == "@":
                splittext = (tweet).split(":")
                username = str(splittext[0]).replace("@", "")
                api.create_friendship(username)
                print ("JUST FOLLOWED " + (username))
            else:
                username = i.user.screen_name
                api.create_friendship(username)
                print ("JUST FOLLOWED " + str(username))

        # This next part favorites tweets if it has to
        if any(k in i.text for k in favKeywords):
            api.create_favorite(i.id)
            print ("JUST FAVORITED " + (i.text))
        # This part waits a bit before moving onto the next one.
        time.sleep(10)#could this be 10 sec? - used to be 60 - get me suspended????


def run():
    for key in ["RT to win", "retweet to win"]:
        print ("************************")
        print ("\n...Refreshing searched tweets...\n")
        print ("************************")
        search(api.search(q=key))


if __name__ == '__main__':
    print ("reminder -- if you run this for too long it will get your account suspended. I'd suggest using it on a 'test account'" \
          "\nand only letting it run for a short time every day.")
    print('starting twitter bot...')
    while True:
        run()
