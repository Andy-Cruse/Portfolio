import pandas as pd
import numpy as np
import requests


file1 = open('data.txt', 'r')
Lines = file1.readlines()

# File used to get subreddit names and member numbers
# needs to be formatted.
count = 0
rows = []
# Strips the newline character
for line in Lines:
    count += 1
    if count % 2 != 0: # original data.txt only has data on odd lines
        row = str(line.strip()).replace(",", "")
        row = row.replace(" - ", ",")
        row = row.replace(" members", "")
        row = row.replace("r/", "")
        rows.append(row)
        print(row) # prints data in csv like format, I just copied and converted to a csv file

subreddit_data = pd.read_csv('subreddit_data.csv')
print(subreddit_data)

# Praw sucks changing to Pushshift API
# # Example showing how this works
# subreddit = reddit.subreddit('DesMoines')
# count = 0
# for submission in subreddit.search("Mom"):
#     print(submission.title)
#     print(count)
#     count += 1

# Going to use comic book character names and search subreddits looking for submissions

dc_comics = pd.read_csv('dc-wikia-data_csv.csv')
marvel_comics = pd.read_csv('marvel-wikia-data_csv.csv')
comics = dc_comics.append(marvel_comics)
comics = comics.reset_index()
comics.columns = comics.columns.str.strip()

# Example pushift api request
r = requests.get('https://api.pushshift.io/reddit/search/comment/?q=science&subreddit=askscience&size=1&metadata=true')
data = r.json()
print(data)

# Get data from each subreddit for each keyword for most popular comic character
# by number of appearances
print(comics.columns.tolist())
comics = comics.sort_values(by="appearances", ascending=False, ignore_index=True)
count_list = []
hero = 0
name = 0
df = pd.DataFrame(columns=subreddit_data.NAME, index= comics.name[:10])
# while name < len(subreddit_data.NAME):
#     while hero < len(comics.name[:10]):
#         print("HERO NAME: " + comics.name[hero])
#         print("CITYNAME: "+subreddit_data.NAME[name])
#         # the comics have this format of hero name followed by their ID, this removes ID
#         head, sep, tail = comics.name[hero].partition('(')
#         print(head)
#         r = requests.get(f'https://api.pushshift.io/reddit/search/comment/?q={head}&subreddit={subreddit_data.NAME[name]}&size=1&metadata=true')
#         if r.status_code == 200:
#             data = r.json()
#             count_list.append(data['metadata']['total_results'])
#             hero += 1
#             print("Loaded " + str(hero) + "/" + str(len(comics.name)))
#             # print(count_list)
#     df[subreddit_data.NAME[name]] = count_list
#     name += 1
#     print("Name value "+str(name))
#     count_list.clear()
#     hero = 0
# df.to_csv("comic_mention.csv")
total = ['total']
comic_mention = pd.read_csv("comic_mention.csv")
for city in subreddit_data.NAME:
    print(subreddit_data[subreddit_data.NAME == city].MEMBERS.values)
    comic_mention[city] = comic_mention[city] / subreddit_data[subreddit_data.NAME == city].MEMBERS.values
    total_mention = np.sum(comic_mention[city])
    total.append(total_mention)
a_series = pd.Series(total, index=comic_mention.columns)
comic_mention = comic_mention.append(a_series, ignore_index=True)
max_total = np.max(total[1:])
max_index = total.index(max_total)
best_city = comic_mention.columns[max_index]
print(best_city)