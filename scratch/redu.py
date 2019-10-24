import json

#with open('data.txt') as json_file:  

data = json.load(open('data.txt'))
for p in data['people']:
    print('Name: ' + p['name'])
    print('Website: ' + p['website'])
    print('From: ' + p['from'])
    print('')
