import json

feed_set1 = {"math.AC", "math.AG", "math.AT"}
feed_set2 = {"math.OC"}
accept_set = set()
with open("/home/k5shao/Downloads/arxiv-meta.json/arxiv-meta.json", "r") as f:
    for line in f:
        a = json.loads(line)
        print(a["id"], a["title"], a["categories"])

        if len(a["categories"].split()) >= 2:
            break
        # id' 'title' 'categories'

