import twint
import pandas as pd
import string
import re
from langdetect import detect_langs
from wordcloud import WordCloud
import itertools
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from collections import Counter
import csv
import operator

#make twitter object
twitter = twint.Config()

#5 mile radius around Clifton, NJ
twitter.Geo = "40.8584, -74.1638, 5 mi"

#tweets from the past 2 months
twitter.Since = "2020-06-01"
twitter.Until = "2020-08-13"

#save as CSV
twitter.Store_csv = True
twitter.Output = "clifton.csv"

#search
twint.run.Search(twitter)

#import csv
tweet = pd.read_csv("clifton.csv")

#delete non-essential columns only collect tweets
words = tweet[['tweet']]

#### Tweets ####

#function to check if string uses english alphabet (doesn't get rid of spanish)
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

#delete non-english alphabet using tweets and tweets with picture links and emojis
for index, row in words.iterrows():
    if isEnglish(row["tweet"]) == False or "pic.twitter" in row["tweet"]:
        words = words.drop(index)

#create csv
words.to_csv("deleteNonEnglishandPic.csv")

#read in csv
tweets = pd.read_csv("deleteNonEnglishandPic.csv", index_col = 0)

#make it a string
tweets = tweets["tweet"].astype(str)

#put into list and flatten
twitter = []
for tweet in tweets:
    twitter.append(tweet.split(" "))

flatten = []
for sublist in twitter:
    for word in sublist:
        flatten.append(word.lower())

#all common words and unnecessary words
s = stopwords.words('english')
more_words = ["would", "really", 'going', 'never', 'think', 'could', 'still', 'thank', 'always', 'something','@plwmpodcast', "that.",'looking', 'fucking', 'getting', "people", "things", 'thing', 'someone', 'thank', 'niggas', 'nigga', 'gonna', 'first', 'please', 'every', 'gotta', 'wanna', 'everything', 'know', "thanks", "actually", 'everyone', "thought", "thing", "anyone"]
for words in more_words:
    s.append(words)

#get rid of spaces
for words in flatten:
    flatten[flatten.index(words)] = words.replace(" ", "")

#make new list to get rid of short words
lst = [words for words in flatten if len(words) > 4]

#get rid of stop words
tw = [words for words in lst if words not in s]

#create a word cloud of the top 75 words and save it
unique_string=(" ").join(tw)
wordcloud = WordCloud(max_font_size=100, max_words=75, background_color="white", width = 1000, height = 500).generate(unique_string)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
wordcloud.to_file("tweets.png")
plt.show()
plt.close()


#counts the frequency of word
counts = Counter(tw)

#deletes words that have a low frequency
selectedKeys = []
valuesToDelete = [1,2,3,4,5,6,7,8,9,10]

for (key, value) in counts.items() :
    if value in valuesToDelete:
        selectedKeys.append(key)

for key in selectedKeys:
    if key in counts:
        del counts[key]

#sorts all dictionary items in ascending order
sorted_d = dict(sorted(counts.items(), key=operator.itemgetter(1),reverse=True))

#bar chart of word frequency
keys = sorted_d.keys()
values = sorted_d.values()

barlist = plt.bar(keys, values)
plt.xticks(rotation=70, fontsize = 8)
plt.suptitle('Tweet Frequency in Clifton, NJ', fontsize=20)
plt.xlabel('Tweet', fontsize=18)
plt.ylabel('Frequency', fontsize=16)

#made important words a different color
barlist[0].set_color('red')
barlist[4].set_color('red')
barlist[10].set_color('red')
barlist[18].set_color('red')
barlist[24].set_color('red')
barlist[30].set_color('red')
barlist[34].set_color('red')
barlist[37].set_color('red')
barlist[43].set_color('red')
plt.tight_layout()
plt.show()
plt.close()