#!/usr/bin/env python
# coding: utf-8

# In[2]:


from csv import reader
with open("hacker_news.csv", "r") as file:
    f = reader(file)
    hn = list(f)
    print(hn[0:5])


# In[4]:


headers = hn[0]
hn.remove(headers)
print(headers)
print(hn[0:5])


# In[7]:


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


# In[8]:


total_ask_comments = 0
for row in ask_posts:
    total_ask_comments += int(row[4])
print(total_ask_comments)
total_show_comments = 0
for row in show_posts:
    total_show_comments += int(row[4])
print(total_show_comments)    


# In[10]:


result = total_ask_comments - total_show_comments
print("total_ask_comments more on", result, "times.")


# In[21]:


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


# In[23]:


avg_by_hour = []
for com in comments_by_hour:
    avg_by_hour.append([com, comments_by_hour[com] / counts_by_hour[com]])
print(avg_by_hour)


# In[24]:


swap_avg_by_hour = []
for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])
print(swap_avg_by_hour)


# In[35]:


sorted_swap = sorted(swap_avg_by_hour, reverse=True)
print("Top 5 Hours for Ask Posts Comments")
top_swap = sorted_swap[0:5]
for swap in top_swap:
    time = dt.datetime.strptime(swap[1], "%H")
    time = dt.datetime.strftime(time, "%H:%M")
    print("{}: {:.2f} average comments per post".format(time, swap[0]))


# In[ ]:




