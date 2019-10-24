import json
json.dumps({
    "name": "Foo Bar",
    "age": 78,
    "friends": ["Jane", "Johni"],
    "balance": 345.80,
    "other_names":("Doe", "Joe"),
    "active":True,
    "spouse":None
    
}, sort_keys=True, indent=4)
