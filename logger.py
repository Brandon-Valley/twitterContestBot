#Efficiency Tip:
# from test.test_import import PycRewritingTests
# every time you write something to a csv, it deletes everything in the csv, because of this, in order to log 
# something you must first record everything already in the csv, then write everything that used to be in the
# csv plus what you are trying to log.  If you are dealing with a csv with a lot of data, recording then re-writing 
# it all will take a lot of time.  Because of this, the most efficient way to do logging is to build up a big list
# of all the data you want to log, then logging it all at once.  Therefore you should try to always use
# logList() instead of logSingle() 

import csv


csvPath = r'C:\Users\Brandon\Documents\Personal Projects\twitterContestBot\tweet_log.csv' #temp, there is a better way to do this


tweetLogDict = {'Time/Date': '11:47pm on saterday',
                'User_Name': '@sagman',     
                'Tweet':     'my name is sagman bardlileriownoaosnfo'}

tweetLogDictList = [{'Time/Date': '11:34pm on monday',
                     'User_Name': '@bob',     
                     'Tweet':     'my name is bob and this is a test'},
                    
                    {'Time/Date': '12:35pm on tuesday',
                     'User_Name': '@jill',     
                     'Tweet':     'my name is jill and im the worst'}]


#------------------------------------------------------PUBLIC------------------------------------------------------#


#logs a list of dicts, each dict = one row, dict = {columb header: data}
#ex:
# tweetLogDictList = [{'Time/Date': '11:34pm on monday',
#                      'User_Name': '@bob',     
#                      'Tweet':     'my name is bob and this is a test'},
#                     
#                     {'Time/Date': '12:35pm on tuesday',
#                      'User_Name': '@jill',     
#                      'Tweet':     'my name is jill and im the worst'}]
def logList(dataDictList, csvPath):
    #build headerList
    headerList = []
    for header, data in dataDictList[0].items():
        headerList.append(header)
        
    #read the csv into a list of dicts (one dict for each row)
    csvData = readCSV(csvPath, headerList)  
     
    #add the data to be logged to the list of csv data
    for dataDict in dataDictList:
        csvData.append(dataDict) 
        
    #write it all back to the csv    
    write2CSV(csvData)       


#should try not to use much, its not very efficient, same thing as logList() but one dict at a time
#ex:
# tweetLogDict = {'Time/Date': '11:47pm on saterday',
#                 'User_Name': '@sagman',     
#                 'Tweet':     'my name is sagman bardlileriownoaosnfo'}
def logSingle(dataDict, csvPath):
    #build headerList
    headerList = []
    for header, data in dataDict.items():
        headerList.append(header)
        
    #read the csv into a list of dicts (one dict for each row)
    csvData = readCSV(csvPath, headerList)  
     
    #add the data to be logged to the list of csv data
    csvData.append(dataDict) 
        
    #write it all back to the csv    
    write2CSV(csvData) 

#------------------------------------------------------PRIVATE------------------------------------------------------#

def readCSV(csvPath, headerList):
    dataDictList = []
    
    with open(csvPath, 'rt') as csvfile:
        csvReader = csv.DictReader(csvfile)
        for row in csvReader:
            rowDict = {}
            for header in headerList:         
                #convert string to dict
                dataStr = row[header]
                rowDict[header] = dataStr
                #headerDataDict = ast.literal_eval(headerdataStr)   
            dataDictList.append(rowDict)              
    return dataDictList


def write2CSV(logDictList):
        with open(csvPath, 'wt') as csvfile:
            fieldnames = []
            for header, data in logDictList[0].items():
                fieldnames.append(header)

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
            writer.writeheader()
            
            #build rowDictList
            rowDictList = []
            rdlPos = 0
            for logDict in logDictList:
                for header, data in logDict.items():
                    if rowDictList == [] or rdlPos > (len(rowDictList) - 1):
                        rowDictList.append({})
                    rowDictList[rdlPos][header] = data
                rdlPos +=1
            #write rows
            for rowDict in rowDictList:
                #print('writing:', rowDict)
                writer.writerow(rowDict)
        csvfile.close()
        
         
logList(tweetLogDictList, csvPath)         
logSingle(tweetLogDict, csvPath)
         
        
        