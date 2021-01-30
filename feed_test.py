import urllib.request
import feedparser

url = 'http://export.arxiv.org/api/query?search_query=all:math.OC&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending'
data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})).read()
feed = feedparser.parse(data)

proxyDict = {"https": "https://13.212.167,205:8080"}
for entry in feed.entries:
    print(entry.id)
    print(entry.title)



'''
    url = "https://scholar.google.com/scholar?q=" + entry.title.replace(" ", "+").replace("\n", "").encode("ascii", errors="ignore").decode()
    print(entry.title)
    data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
    index = data.find(b'Cited by ') + 9
    if index != 8:
        print(''.join(filter(str.isdigit, str(data[index:index+7]))))
    else:
        print(0, "not found")
    time.sleep(3)

'''
'''
import urllib.request

import time
import feedparser

# Base api query url
base_url = 'http://export.arxiv.org/api/query?';

# Search parameters
search_query = urllib.parse.quote("ti:machine learning")
i = 0
results_per_iteration = 1000
wait_time = 3
papers = []
year = ""
print('Searching arXiv for %s' % search_query)

while (year != "2018"):  # stop requesting when papers date reach 2018
    print("Results %i - %i" % (i, i + results_per_iteration))

    query = 'search_query=%s&start=%i&max_results=%i&sortBy=submittedDate&sortOrder=descending' % (search_query,
                                                                                                   i,
                                                                                                   results_per_iteration)

    # perform a GET request using the base_url and query
    response = urllib.request.urlopen(base_url + query).read()

    # parse the response using feedparser
    feed = feedparser.parse(response)
    # Run through each entry, and print out information
    for entry in feed.entries:
        # print('arxiv-id: %s' % entry.id.split('/abs/')[-1])
        # print('Title:  %s' % entry.title)
        # feedparser v4.1 only grabs the first author
        # print('First Author:  %s' % entry.author)
        paper = {}
        paper["date"] = entry.published
        year = paper["date"][0:4]
        paper["title"] = entry.title
        paper["first_author"] = entry.author
        paper["summary"] = entry.summary
        papers.append(paper)
    # Sleep a bit before calling the API again
    print('Bulk: %i' % 1)
    i += results_per_iteration
    time.sleep(wait_time)
    
    '''