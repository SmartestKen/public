import urllib.request
from xml.etree import ElementTree
from datetime import datetime, timedelta
# url = 'http://export.arxiv.org/api/query?search_query=all:math.OC&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending'
# find a previous date from counter

date = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
url = "http://export.arxiv.org/oai2?verb=ListRecords&set=math&from="+date+"&until="+date+"&metadataPrefix=arXivRaw"
data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})).read()

feed_set1 = set("math.AC", "math.AG", "math.AT")
feed_list2 =




prefix = '{http://www.openarchives.org/OAI/2.0/}'
prefix2 = '{http://arxiv.org/OAI/arXivRaw/}'
prefix3 = "https://arxiv.org/abs/"


for child in ElementTree.fromstring(data).find(prefix + "ListRecords"):
    info = child.find(prefix+"metadata").find(prefix2+"arXivRaw")


    print(info.find(prefix2 + "categories").text.split())
    # make a feasible filter
    print(prefix3 + info.find(prefix2 + "id").text)
    print(info.find(prefix2+"title").text)

