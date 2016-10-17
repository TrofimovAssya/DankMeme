
# coding: utf-8

# In[31]:

import requests
from bs4 import BeautifulSoup
import cPickle as pickle


meme_corpus = []

for i in xrange(1001,2000):
    print ("page " + str(i))
    page = requests.get("https://memegenerator.net/The-Most-Interesting-Man-In-The-World/images/popular/alltime/page/"+str(i))
    print(page.status_code)
    content = BeautifulSoup(page.content)
    imgs = content.select('li div a img')
    for img in imgs:
        meme_corpus.append(img['alt'].split("The Most Interesting Man In The World - ")[1])
        
pickle.dump(meme_corpus,open("mostinterestingman2.p","wb"))





