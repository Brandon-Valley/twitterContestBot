# big thanks to Robbie Barrat for writing some helpful code and github user 'timster' for optimizing a lot of rough bits
import tweepy
import time



def makeAfuss():
    numLines = 20
    bigStr = '*******************************************'
    for x in range(numLines):
        print(bigStr)
        
#stuff to do:
#make it follow any other user mentioned in a tweet
#fix misc errors
#play with timer speed
#add ability to tag friends
#split stuff up for multiple bot usage
#maybe add something so even if you rt a new contest, if you are already follow them, dont follow again - is this a real problem???
#once it can run for a day - make it write the time/other data to exel sheet and set it up to graph stuff like rt's per hour to see most active times each day
#what do they mean my "show proof"?  need to make something for this???
#why isnt that list of "keys" in run the same as rtKeywords?  am i missing out on searches or avoiding bad ones? need to change???
#add check for "RT+F", RT&F, FLW & RT, #FLW us both & #RT, (heart emoji) + RT
#add bot-spoter detection
#add false positive thing
#what happens if you aouto block anyone who retweets something from a known bot spoter ie infirior bots? - preformance increace?

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

followKeywords = ['follow']

favKeywords = ['fav']

bannedwords = ["vote"]
 
knownBotSpoters = ['nirvana_wright', 'B0tSp0tterB0t', 'followandrt2win', 'Shart_ebooks',
                   '@botfinder_g', 'B0TTT0M', '_aekkaphon']

KnownTweepyErrors = ["code': 108, 'message': 'Cannot find specified user.",
                "'message': 'You have already favorited this status.', 'code': 139}",
                "code': 139, 'message': 'You have already favorited this status."]



def knownBotSpoter(i):
    # get username - check the actual contest-holder, instead of some random person who retweeted their contest
    tweet = i.text
    if tweet[0:3] == "RT ":
        tweet = tweet[3:]
    if tweet[0] == "@":
        splittext = (tweet).split(":")
        username = str(splittext[0]).replace("@", "")
    else:
        username = i.user.screen_name
    #check if OG poster is a known bot spotter
    for knownBotSpoterUsername in knownBotSpoters:
        if username == knownBotSpoterUsername:
            return True
    return False
    
    
def search(twts):
    for i in twts:
        if not any(k in i.text.lower() for k in rtKeywords) or any(k in i.text.lower() for k in bannedwords or knownBotSpoter(i)):
            continue
        # Retweets
        try:
            api.retweet(i.id)
            print ("JUST RETWEETED " + (i.text))
            #print('TEST- i.text.lower():', i.text.lower())#!!!!!!!!!!!!!!!!!!!!!!!!!
        except:
            print ("Hm... Something went wrong. - probably already retweeted this.")
        # Follows
        if any(k in i.text.lower() for k in followKeywords):
            # follow the actual contest-holder, instead of some random person who retweeted their contest
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
            #follows 

        # favorites tweets if needed
        if any(k in i.text.lower() for k in favKeywords):
           # try:#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
         api.create_favorite(i.id)
#                 print ("JUST FAVORITED " + (i.text))
#             except:
#                 print('error catch -- just skipped over a "you already favorited this status" error')
        # waits a bit before moving onto the next one.
        time.sleep(10)#could this be 10 sec? - used to be 60 - get me suspended????


def run():#clean this up!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        for key in ["RT to win", "retweet to win"]:#why isnt this the same as rtKeywords?????????????
            print ("************************")
            print ("\n...Refreshing searched tweets...\n")
            print ("************************")
            search(api.search(q=key))
    except tweepy.TweepError as e:
        if e in knownTweepyErrors:
            makeAfuss()
            print('error catch -- tweepy error  -- %s -- restarting twitterbot', e.message)
            run()
    except UnicodeEncodeError as e:
        makeAfuss() 
        print('error catch -- UnicodeEncoderError -- %s -- restarting twitterbot', e.message)
        run()


if __name__ == '__main__':
    print ("reminder -- if you run this for too long it will get your account suspended. I'd suggest using it on a 'test account'" \
          "\nand only letting it run for a short time every day.")
    print('starting twitter bot...')
    while True:
        run()
