import urllib.request
from xml.etree import ElementTree

# url = 'http://export.arxiv.org/api/query?search_query=all:math.OC&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending'
# find a previous date from counter
url = "http://export.arxiv.org/oai2?verb=ListRecords&set=math&from=2015-01-27&until=2015-01-27&metadataPrefix=arXivRaw"
data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})).read()



prefix = '{http://www.openarchives.org/OAI/2.0/}'
prefix2 = '{http://arxiv.org/OAI/arXivRaw/}'
prefix3 = "https://arxiv.org/abs/"


for child in ElementTree.fromstring(data).find(prefix + "ListRecords"):
    info = child.find(prefix+"metadata").find(prefix2+"arXivRaw")
    print(info.find(prefix2+"categories").text)

    # make a feasible filter
    print(prefix3 + info.find(prefix2 + "id").text)
    print(info.find(prefix2+"title").text)

