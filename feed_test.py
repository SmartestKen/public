
import feedparser
url_set1 = set()
feed_list1 = ["math.AC"]
for category in feed_list1:
    feed = feedparser.parse("http://arxiv.org/rss/" + category)
    print(feed)

    exit(0)
    url_set1.update([x.id for x in feed])

url_set = set()
feed = feedparser.parse("http://arxiv.org/rss/" + "math.OC").entries
url_set.update([[x.id, x.title] for x in feed])

url_set.update(url_set1)
print(url_set)





