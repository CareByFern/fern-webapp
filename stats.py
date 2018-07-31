import csv
import collections
import os

responses = collections.defaultdict(lambda: collections.defaultdict(int))


r = csv.reader(open(os.path.expanduser('~/Downloads/Responses to Technology Screener - Sheet.csv')))
# Skip first line
headers1 = next(r)
headers2 = next(r)

for line in r:
    for i in range(len(line)):
        columnName = '[%s] %s %s' % (i, headers1[i], headers2[i])
        responses[columnName][line[i]] += 1
#        print(columnName)
    #print(line)


for k,v in responses.items():
    print(k)
    if len(v) > 10:
        print('- truncated')
        continue
    for k,v in sorted(v.items()):
        print('- %s: %s' % (k,v))
