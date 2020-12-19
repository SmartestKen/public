with open("/home/public/arxiv_feed") as f:
    content = f.readlines()

from datetime import date
today_date = str(date.today())
if content[-1].strip() == "--------end of " + today_date + "--------":
    print("feed already updated")
else:

    import feedparser
    url_set1 = set()


    feed_list1 = ["math.AC", "math.AG", "math.CO", "math.RT", "math.AT",
                  "math.CT", "math.RA", "math.QA", "math.KT", "math.GR"]
    for category in feed_list1:
        feed = feedparser.parse("http://arxiv.org/rss/" + category).entries
        url_set1.update([x.id for x in feed])

    url_set2 = set()
    feed_list2 = ["cs.LG", "cs.AI", "stat.ML", "math.OC", "cs.CV",
                  "cs.MS", "cs.NE", "cs.SC", "eess.SY"]
    for category in feed_list2:
        feed = feedparser.parse("http://arxiv.org/rss/" + category).entries
        url_set2.update([x.id for x in feed])



    url_set = set.intersection(url_set1, url_set2)

    with open('/home/public/arxiv_feed', 'a') as f:
        for item in list(url_set.difference({x.strip() for x in content})):
            f.write("%s\n" % item)
        f.write("--------end of " + today_date + "--------\n")






