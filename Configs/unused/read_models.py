import json

with open('data.txt') as json_file:  
    data = json.load(json_file)
    for p in data['models']:
        print('Name: ' + p['name'])
