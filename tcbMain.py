import os
from multiprocessing.dummy import Pool as ThreadPool 
import itertools

import tweetBot
import logger


def startBot(runTime, bot):
    bot.start(runTime)
    
def hour2sec(hours):
    return hours * 3600

#control constants
MAX_BOT_RUNTIME = 3 #hours
BOT_COOL_DOWN_TIME = 2 #hours
NUM_THREADS = 2 #what should this number be/what does it really mean?????????????????????????

full_path = os.path.realpath(__file__)
credPath =  os.path.dirname(full_path) + '\\credentials.csv'

botCredentials = logger.readCSV(credPath)

numBots = len(botCredentials)
print('Number of Bots:', numBots)

#make bots
bots = []
for bot in botCredentials:
    credentials = {'CONSUMER_KEY':      bot['CONSUMER_KEY'],
                   'CONSUMER_SECRET':   bot['CONSUMER_SECRET'],
                   'ACCESS_KEY':        bot['ACCESS_KEY'],
                   'ACCESS_SECRET':     bot['ACCESS_SECRET']}
    
    newBot = tweetBot.tweetBot(bot['id'], credentials)
    bots.append(newBot)
    
#run bots
runTime = hour2sec(MAX_BOT_RUNTIME)
pool = ThreadPool(NUM_THREADS) 
# results = pool.map(startBot, MAX_BOT_RUNTIME, bots)
results = pool.starmap(startBot, zip(itertools.repeat(runTime), bots))
print(results)
    


    
#run bots
# bots[0].start()
# bots[1].start()






# 
# 
# full_path = os.path.realpath(__file__)
# bot0path =  os.path.dirname(full_path) + '\\bot_data\\bot_0'
# 
# tb0 = tweetBot.tweetBot(bot0path)
# 
# 
# print(tb0.dataPath)
# print(tb0.CONSUMER_KEY)