import time
from multiprocessing.dummy import Pool as ThreadPool 

def retNum(num):
    return(num)

numList = [1,2,3]

# make the Pool of workers
pool = ThreadPool(4) 

# open the urls in their own threads
# and return the results
results = pool.map(retNum, numList)
print(results)

# close the pool and wait for the work to finish 
pool.close() 
pool.join() 

print(time.time())
beforeTime = time.time()
time.sleep(10)
afterTime = time.time()

sleepTime = beforeTime - afterTime

print('sleep time:', sleepTime)