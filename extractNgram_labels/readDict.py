import json
import heapq
import matplotlib.pyplot as plt
def findNMaxinDict(d,N):
    res = [(0,'dummy') for i in range(N)]
    heapq.heapify(res)
    mn = 0
    for k in d:
        if d[k] > mn:
            heapq.heapreplace(res, (d[k],k))
            mn,key_mn = heapq.heappop(res)
            heapq.heappush(res,(mn,key_mn))
    return res



if __name__ == '__main__':

    with open('ngramDict.json','r') as json_data:
        ngramDict = json.load(json_data)
        for i in range(len(ngramDict)):
            res = findNMaxinDict(ngramDict[i],100)
            res.sort()
            print res
            freq = [ngramDict[i][k] for k in ngramDict[i]]
            freq.sort()

            print freq
            # tail = 0.3
            # plt.plot(freq[0:int(len(freq)*tail)])
            # plt.show()
