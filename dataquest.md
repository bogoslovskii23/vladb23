

```python
from csv import reader
with open("hacker_news.csv", "r") as file:
    f = reader(file)
    hn = list(f)
    print(hn[0:5])
```

    [['id', 'title', 'url', 'num_points', 'num_comments', 'author', 'created_at'], ['12224879', 'Interactive Dynamic Video', 'http://www.interactivedynamicvideo.com/', '386', '52', 'ne0phyte', '8/4/2016 11:52'], ['10975351', 'How to Use Open Source and Shut the Fuck Up at the Same Time', 'http://hueniverse.com/2016/01/26/how-to-use-open-source-and-shut-the-fuck-up-at-the-same-time/', '39', '10', 'josep2', '1/26/2016 19:30'], ['11964716', "Florida DJs May Face Felony for April Fools' Water Joke", 'http://www.thewire.com/entertainment/2013/04/florida-djs-april-fools-water-joke/63798/', '2', '1', 'vezycash', '6/23/2016 22:20'], ['11919867', 'Technology ventures: From Idea to Enterprise', 'https://www.amazon.com/Technology-Ventures-Enterprise-Thomas-Byers/dp/0073523429', '3', '1', 'hswarna', '6/17/2016 0:01']]



```python
headers = hn[0]
hn.remove(headers)
print(headers)
print(hn[0:5])
```

    ['id', 'title', 'url', 'num_points', 'num_comments', 'author', 'created_at']
    [['12224879', 'Interactive Dynamic Video', 'http://www.interactivedynamicvideo.com/', '386', '52', 'ne0phyte', '8/4/2016 11:52'], ['10975351', 'How to Use Open Source and Shut the Fuck Up at the Same Time', 'http://hueniverse.com/2016/01/26/how-to-use-open-source-and-shut-the-fuck-up-at-the-same-time/', '39', '10', 'josep2', '1/26/2016 19:30'], ['11964716', "Florida DJs May Face Felony for April Fools' Water Joke", 'http://www.thewire.com/entertainment/2013/04/florida-djs-april-fools-water-joke/63798/', '2', '1', 'vezycash', '6/23/2016 22:20'], ['11919867', 'Technology ventures: From Idea to Enterprise', 'https://www.amazon.com/Technology-Ventures-Enterprise-Thomas-Byers/dp/0073523429', '3', '1', 'hswarna', '6/17/2016 0:01'], ['10301696', 'Note by Note: The Making of Steinway L1037 (2007)', 'http://www.nytimes.com/2007/11/07/movies/07stein.html?_r=0', '8', '2', 'walterbell', '9/30/2015 4:12']]



```python
ask_posts = []
show_posts = []
other_posts = []
for row in hn:
    title = row[1].lower()
    if title.startswith("ask hn"):
        ask_posts.append(row)
    elif title.startswith("show hn"):
        show_posts.append(row)
    else:
        other_posts.append(row)
print(len(ask_posts), len(show_posts), len(other_posts))
```

    1744 1162 17194



```python
total_ask_comments = 0
for row in ask_posts:
    total_ask_comments += int(row[4])
print(total_ask_comments)
total_show_comments = 0
for row in show_posts:
    total_show_comments += int(row[4])
print(total_show_comments)    
```

    24483
    11988



```python
result = total_ask_comments - total_show_comments
print("total_ask_comments more on", result, "times.")
```

    total_ask_comments more on 12495 times.



```python
import datetime as dt
result_list = []
for row in ask_posts:
    result_list.append([row[6], int(row[4])])
counts_by_hour = dict()
comments_by_hour = dict()
for row in result_list:
    date = dt.datetime.strptime(row[0], "%m/%d/%Y %H:%M")
    hour = dt.datetime.strftime(date, "%m/%d/%Y %H:%M")
    hour = hour[-5:-3]
    if hour not in counts_by_hour.keys():
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = row[1]
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += row[1]
```


```python
avg_by_hour = []
for com in comments_by_hour:
    avg_by_hour.append([com, comments_by_hour[com] / counts_by_hour[com]])
print(avg_by_hour)
```

    [['09', 5.5777777777777775], ['21', 16.009174311926607], ['18', 13.20183486238532], ['01', 11.383333333333333], ['17', 11.46], ['15', 38.5948275862069], ['19', 10.8], ['07', 7.852941176470588], ['00', 8.127272727272727], ['06', 9.022727272727273], ['16', 16.796296296296298], ['02', 23.810344827586206], ['04', 7.170212765957447], ['20', 21.525], ['08', 10.25], ['23', 7.985294117647059], ['10', 13.440677966101696], ['14', 13.233644859813085], ['12', 9.41095890410959], ['05', 10.08695652173913], ['13', 14.741176470588234], ['11', 11.051724137931034], ['03', 7.796296296296297], ['22', 6.746478873239437]]



```python
swap_avg_by_hour = []
for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])
print(swap_avg_by_hour)
```

    [[5.5777777777777775, '09'], [16.009174311926607, '21'], [13.20183486238532, '18'], [11.383333333333333, '01'], [11.46, '17'], [38.5948275862069, '15'], [10.8, '19'], [7.852941176470588, '07'], [8.127272727272727, '00'], [9.022727272727273, '06'], [16.796296296296298, '16'], [23.810344827586206, '02'], [7.170212765957447, '04'], [21.525, '20'], [10.25, '08'], [7.985294117647059, '23'], [13.440677966101696, '10'], [13.233644859813085, '14'], [9.41095890410959, '12'], [10.08695652173913, '05'], [14.741176470588234, '13'], [11.051724137931034, '11'], [7.796296296296297, '03'], [6.746478873239437, '22']]



```python
sorted_swap = sorted(swap_avg_by_hour, reverse=True)
print("Top 5 Hours for Ask Posts Comments")
top_swap = sorted_swap[0:5]
for swap in top_swap:
    time = dt.datetime.strptime(swap[1], "%H")
    time = dt.datetime.strftime(time, "%H:%M")
    print("{}: {:.2f} average comments per post".format(time, swap[0]))
```

    Top 5 Hours for Ask Posts Comments
    15:00: 38.59 average comments per post
    02:00: 23.81 average comments per post
    20:00: 21.52 average comments per post
    16:00: 16.80 average comments per post
    21:00: 16.01 average comments per post



```python

```
