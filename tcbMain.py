import os
from multiprocessing.dummy import Pool as ThreadPool 
import itertools

import tweetBot
import logger


def startBot(runTime, bot):
    bot.start(runTime)


MAX_BOT_RUNTIME = 60 #seconds -- will be hours in the end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
MAX_BOT_RUNS_PER_DAY = None #not used yet!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
    

def getID(bot):
    return bot.id

 
# results = []
# for item in my_array:
# results.append(my_function(item)) 
    
# from multiprocessing.dummy import Pool as ThreadPool 
# pool = ThreadPool(2) 
# results = pool.map(my_function, my_array)
        

pool = ThreadPool(2) 
# results = pool.map(startBot, MAX_BOT_RUNTIME, bots)
results = pool.starmap(startBot, zip(itertools.repeat(MAX_BOT_RUNTIME), bots))
print(results)
    


    
#run bots
# bots[0].start()
# bots[1].start()


def getID(bot):
    return bot.id





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