import csv
import json



with open('/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/baselineTrail/shrinkLevel2/ngramDictShrinkedLevel2.json','r') as json_data:
     ngramDict = json.load(json_data)



with open('/Users/jinny/CMU/2017Fall/10-605/yelp challenge/10805-YelpChallenge/rawNgram/1gram.csv','rU') as csvfile:
     reader = csv.reader(csvfile, delimiter='\t')
     features = set(ngramDict[0].keys())
     print "1gramfeatures:" ,len(features)
     with open('1gramShrinkLevel2.csv','wb') as shrinkfile:
         wtr = csv.writer(shrinkfile,delimiter='\t',lineterminator='\n')
         count = 0
         for row in reader:
             count += 1
             if count % 1000 == 0:
                 print count
             if(len(row)<2):
                print "rowIndex: ",count
                print row
                break
             review_id  = row[0]


             newrow = set(row[1].strip().split()) & features
             strNewrow = ' '.join(newrow)

             # if count > 5:
             #     break
             store = [review_id, strNewrow]
             wtr.writerow(store)
