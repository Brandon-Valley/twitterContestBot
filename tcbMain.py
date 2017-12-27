import os

import tweetBot
import logger



full_path = os.path.realpath(__file__)
credPath =  os.path.dirname(full_path) + '\\credentials.csv'

botCredentials = logger.readCSV(credPath)

print(botCredentials)

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
bots[0].start()








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