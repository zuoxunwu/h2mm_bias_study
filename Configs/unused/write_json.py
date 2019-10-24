import json

data = {}  
data['models'] = []  
data['models'].append({  
    'name': 'func1'
})
data['models'].append({  
    'name': 'func2'
})

with open('data.txt', 'w') as outfile:  
    json.dump(data, outfile)
