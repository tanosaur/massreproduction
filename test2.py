import json

with open('basic.mr', mode='r') as f:
    thing=json.load(f)

print(thing)
