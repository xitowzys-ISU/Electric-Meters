import json


with open('./logs/logs.log') as f:
    for line in f:
        pass
    json_line = json.loads(line)

print(json_line['record']['message'])