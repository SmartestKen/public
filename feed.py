with open("/home/public/arxiv_feed") as f:
    content = f.readlines()

import datetime
date_obj = datetime.datetime.today()
weekday_list = ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"]
today_date = str(date_obj.date()) + " " + str(weekday_list[date_obj.weekday()])

if content[-1].strip() == "--------end of " + today_date + "--------":
    print("feed already updated")
else:

    import feedparser
    url_set1 = set()


    feed_list1 = ["math.AC", "math.AG", "math.CO", "math.RT", "math.AT",
                  "math.CT", "math.RA", "math.QA", "math.KT", "math.GR", "cs.MS"]
    for category in feed_list1:
        feed = feedparser.parse("http://arxiv.org/rss/" + category).entries
        url_set1.update([x.id for x in feed])

    url_set2 = set()
    feed_list2 = ["cs.LG", "cs.AI", "stat.ML", "math.OC", "cs.SC", "eess.SY"]
    for category in feed_list2:
        feed = feedparser.parse("http://arxiv.org/rss/" + category).entries
        url_set2.update([x.id for x in feed])



    url_set = set.intersection(url_set1, url_set2)


    with open('/home/private/daily_log', 'a') as f:
        f.write("-------- " + today_date + "--------\n")


    with open('/home/public/arxiv_feed', 'a') as f:
        for item in list(url_set.difference({x.strip() for x in content})):
            f.write("%s\n" % item)
        f.write("--------end of " + today_date + "--------\n")






