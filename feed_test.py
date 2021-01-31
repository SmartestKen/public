import urllib.request
from xml.etree import ElementTree
from datetime import datetime, timedelta
# url = 'http://export.arxiv.org/api/query?search_query=all:math.OC&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending'
# find a previous date from counter
import time

for days_from_today in range(1, 1001):
    date = (datetime.today() - timedelta(days=days_from_today)).strftime('%Y-%m-%d')
    url = "http://export.arxiv.org/oai2?verb=ListRecords&set=math&from="+date+"&until="+date+"&metadataPrefix=arXivRaw"
    data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})).read()

    feed_set1 = {"math.AC", "math.AG", "math.AT"}
    feed_set2 = {"math.OC"}
    accept_set = set()

    print(date)
    print(url)
    print(data)

    prefix = '{http://www.openarchives.org/OAI/2.0/}'
    prefix2 = '{http://arxiv.org/OAI/arXivRaw/}'
    prefix3 = "https://arxiv.org/abs/"



    for child in (ElementTree.fromstring(data).find(prefix + "ListRecords") or []):
        info = child.find(prefix+"metadata").find(prefix2+"arXivRaw")


        given_set = set(info.find(prefix2 + "categories").text.split())
        if bool(given_set & feed_set1) and bool(given_set & feed_set2):
            # decide if collect all to print to file and print and write
            # make a feasible filter
            accept_set.add(prefix3 + info.find(prefix2 + "id").text + "\n"
                           + info.find(prefix2+"title").text + "\n")

    with open('/home/public/arxiv_collection', 'a') as f:
        for item in list(accept_set):
            f.write("%s" % item)
        if len(accept_set) > 0:
            f.write("--------end of " + date + "--------\n")
        else:
            print("No records today, skipping")

    time.sleep(10)