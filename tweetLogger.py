#tweetLogger #should this file be combined with something else?????
import logger
import datetime
import os



def logEvent(botID, text, rt, flw, fav):
    full_path = os.path.realpath(__file__)
    logPath =  os.path.dirname(full_path) + '\\tweet_logs\\' + (botID + '_tweet_log.csv')

    now = datetime.datetime.now()
    
    tweetInfo = {'year':        now.year,
                 'month':       now.month,
                 'day':         now.day,
                 'hour':        now.hour,
                 'minute':      now.minute,
                 'second':      now.second,
                 'microsecond': now.microsecond,
                 
                 'tweet':       text,
                 're-tweeted':  rt,
                 'followed':    flw,
                 'favorited':   fav}
    
    logger.logSingle(tweetInfo, logPath)
    



