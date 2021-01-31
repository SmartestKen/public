import json

feed_set1 = {"math.AC", "math.AG", "math.AT"}
feed_set2 = {"math.OC"}
accept_set = set()
id_prefix = "https://arxiv.org/abs/"
with open("/home/k5shao/Downloads/arxiv-meta.json/arxiv-meta.json", "r") as f:
    for line in f:
        a = json.loads(line)
        art_set = set([x.strip() for x in a["categories"].split()])
        if bool(art_set & feed_set1) and bool(art_set & feed_set2):
            print(a["id"], a["title"])
            accept_set.add(id_prefix + a["id"] + "\n"
                           + a["title"] + "\n")

with open('/home/public/arxiv_collection2', 'w') as f:
    for item in list(accept_set):
        f.write("%s" % item)
