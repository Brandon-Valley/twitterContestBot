import tweepy
import time
import tweetLogger

import logger #just for testing!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#set stuff up  GONNA NEED TO MOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
# api = tweepy.API(auth)


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



class tweetBot:
    def __init__(self, id, credentials):
        self.stopBot = False
        self.id = id
        
#         botFollowers = 'bot_0_followers'
#         
#         from followers import botFollowers
#         
#         print(logger.readCSV)
        
        self.CONSUMER_KEY =    credentials['CONSUMER_KEY']
        self.CONSUMER_SECRET = credentials['CONSUMER_SECRET']
        self.ACCESS_KEY =      credentials['ACCESS_KEY']
        self.ACCESS_SECRET =   credentials['ACCESS_SECRET']
        
        print(self.id)
        
        #set stuff up
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        self.api = tweepy.API(auth)

        
    def knownBotSpoter(self, i):
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


    def search(self, twts):
        for i in twts:
            #vars for tweetLogger
            rt = False
            flw = False
            fav = False
            
            if not any(k in i.text.lower() for k in rtKeywords) or any(k in i.text.lower() for k in bannedwords) or (self.knownBotSpoter(i)):
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
                    self.api.create_friendship(username)
                    print ("JUST FOLLOWED " + (username))
                    flw = True
                else:
                    username = i.user.screen_name
                    self.api.create_friendship(username)
                    print ("JUST FOLLOWED " + str(username))
                    flw = True
                #follows 
    
            # favorites tweets if needed
            if any(k in i.text.lower() for k in favKeywords):
              self.api.create_favorite(i.id)
              print ("JUST FAVORITED " + (i.text))
              fav = True
              
            tweetLogger.logEvent(self.id, i.text, rt, flw, fav)
              
            # waits a bit before moving onto the next one.
            time.sleep(10)#could this be 10 sec? - used to be 60 - get me suspended????
            
            
    def run(self):#clean this up!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        try:
            for key in ["RT to win", "retweet to win"]:#why isnt this the same as rtKeywords?????????????
                print ("************************")
                print ("\n...Refreshing searched tweets...\n")
                print ("************************")
                self.search(self.api.search(q=key))
        except tweepy.TweepError as e:
            if e in knownTweepyErrors:
                print('error catch -- tweepy error  -- %s -- restarting twitterbot', e.message)
                self.run()
        except UnicodeEncodeError as e:
            print('error catch -- UnicodeEncoderError -- %s -- restarting twitterbot', e.message)
            self.run()
            
    
    def start(self):
        self.stopBot = False
        print ("reminder -- if you run this for too long it will get your account suspended. I'd suggest using it on a 'test account'" \
              "\nand only letting it run for a short time every day.")
        print('starting twitter bot...')
        while self.stopBot == False:
            self.run()
            
            
    def stop(self):
        self.stopBot = True
        
        
        