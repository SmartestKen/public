import json

with open("/home/k5shao/Downloads/arxiv-meta.json/arxiv-meta.json", "r") as f:
    for line in f:
        print(line)
        a = json.loads(line)
        print(a["id"])
        print(a.keys())
        break


