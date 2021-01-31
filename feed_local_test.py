import json

feed_set1 = {"math.AC", "math.AG", "math.AT"}
feed_set2 = {"math.OC"}
accept_set = set()
id_prefix = "https://arxiv.org/abs/"
scholar_prefix = "https://scholar.google.com/scholar?q="
with open("/home/k5shao/Downloads/arxiv-meta.json/arxiv-meta.json", "r") as f:
    for line in f:
        a = json.loads(line)
        art_set = set([x.strip() for x in a["categories"].split()])
        if bool(art_set & feed_set1) and bool(art_set & feed_set2):
            print(a["id"], a["title"])

            embed_id = id_prefix + a["id"]
            embed_title = scholar_prefix + a["title"].replace(" ", "+")
            accept_set.add('<a href=' + embed_id +'>' +a['id'] + '</a>' + "<br />\n"
                           + '<a href=' + embed_title +'>' +a['title'] + '</a>' + "<br />\n")

with open('/home/public/arxiv_collect.html', 'w') as f:
    f.write("<!DOCTYPE html><br />\n<head><br />\n")
    for item in list(accept_set):
        f.write("%s" % item)
    f.write("</head>")