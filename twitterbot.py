# big thanks to Robbie Barrat for writing some helpful code and github user 'timster' for optimizing a lot of rough bits
import tweepy
import time
import tweetLogger



def makeAfuss():
    numLines = 20
    bigStr = '*******************************************'
    for x in range(numLines):
        print(bigStr)
        
#stuff to do:
#make it follow any other user mentioned in a tweet
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
#When you establish your API instance include the wait_on_rate_limit parameter (The docs show, it defaults to False). You can also add the notify parameter so you know when you're approaching the limit. http://docs.tweepy.org/en/latest/api.html
#look into wait_on_rate_limit


#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'MEpbDNplsX724pFmaKtTjlMFW' #keep the quotes, enter your consumer key
CONSUMER_SECRET = 'BEIyPrCYzWe8X65fArKE65cXAkLtyUd8RAYlLllHrw4ubiND9T'#keep the quotes, enter your consumer secret key
ACCESS_KEY = '932834480406122497-kEdX6h2yZ7ocWhEgVznG22My7qbeLx5'#keep the quotes, enter your access token
ACCESS_SECRET =  '0hjm4BHFfCiHgNwNVccNw66puL0ZN22hwGinrtdjrW2d6'#keep the quotes, enter your access token secret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)




rtKeywords = ["rt to", "rt and win", "retweet and win",
              "rt for", "rt 4", "retweet to"]

followKeywords = ['follow', 'flw']

favKeywords = ['fav', 'favorite', 'like']

bannedwords = ["vote"]
 
knownBotSpoters = ['nirvana_wright', 'B0tSp0tterB0t', 'followandrt2win', 'Shart_ebooks',
                   'botfinder_g', 'B0TTT0M', '_aekkaphon', 'RealBotSp0tter', 'b0ttt0m', 
                   'jflessauSpam', 'b0ttem', 'BotSp0tterBot', 'bottybotbotl', 
                   'RealBotSpotter', 'bottybotbotl', 'RealB0tSpotter', 'BotSpotterBot',
                   'bottybotbotl', 'jflessauSpam', 'lvbroadcasting' ]

knownTweepyErrors = ["code': 108, 'message': 'Cannot find specified user.",
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
            print('GOTCHA! -- Just spotted a knownBotSpoter:', username)
            return True
    return False
    
    
def search(twts):
    for i in twts:
        #vars for tweetLogger
        rt = False
        flw = False
        fav = False
        
        if not any(k in i.text.lower() for k in rtKeywords) or any(k in i.text.lower() for k in bannedwords) or (knownBotSpoter(i)):
            continue
        # Retweets
        try:
            api.retweet(i.id)
            print ("JUST RETWEETED " + (i.text))
            rt = True

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
                flw = True
            else:
                username = i.user.screen_name
                api.create_friendship(username)
                print ("JUST FOLLOWED " + str(username))
                flw = True
            #follows 

        # favorites tweets if needed
        if any(k in i.text.lower() for k in favKeywords):
          api.create_favorite(i.id)
          print ("JUST FAVORITED " + (i.text))
          fav = True
          
        tweetLogger.logEvent(i.text, rt, flw, fav)
          
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
            makeAfuss()#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            print('error catch -- tweepy error  -- %s -- restarting twitterbot', e.message)
            run()
    except UnicodeEncodeError as e:
        makeAfuss() #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print('error catch -- UnicodeEncoderError -- %s -- restarting twitterbot', e.message)
        run()


if __name__ == '__main__':
    print ("reminder -- if you run this for too long it will get your account suspended. I'd suggest using it on a 'test account'" \
          "\nand only letting it run for a short time every day.")
    print('starting twitter bot...')
    while True:
        run()
