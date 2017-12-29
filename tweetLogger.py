#tweetLogger #should this file be combined with something else?????
import logger
import datetime
import os



def logEvent(botID, username, text, rt, flw, fav):
    full_path = os.path.realpath(__file__)
    twtLogPath =  os.path.dirname(full_path) + '\\tweet_logs\\' + (botID + '_tweet_log.csv')
    flwLogPath =  os.path.dirname(full_path) + '\\follow_lists\\' + (botID + '_follow_list.csv')

    now = datetime.datetime.now()
    
    tweetInfo = {'year':        now.year,
                 'month':       now.month,
                 'day':         now.day,
                 'hour':        now.hour,
                 'minute':      now.minute,
                 'second':      now.second,
                 'microsecond': now.microsecond,
                 
                 'username':    username,
                 'tweet':       text,
                 're-tweeted':  rt,
                 'followed':    flw,
                 'favorited':   fav}
    
    logger.logSingle(tweetInfo, twtLogPath)
    
    if flw == True:
        flwInfo = {'following':  username}
        logger.logSingle(flwInfo, flwLogPath)
    
#this is the most ineffiecient thing ever please change this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#this is a bandaid solution !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def logUnfollow(botID, username):
    full_path = os.path.realpath(__file__)
    flwLogPath =  os.path.dirname(full_path) + '\\follow_lists\\' + (botID + '_follow_list.csv')
    flwLog = logger.readCSV(flwLogPath)

    for rowDict in flwLog:
        if username in rowDict['following']:
            flwLog.remove(rowDict)
            
    logger.write2CSV(flwLog, flwLogPath)
    
    



