#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import random
from flask import Flask


# In[2]:


url_base = 'http://localhost:8080/api'
profiles = '/profiles?pageNumber={}&pageSize={}'
latests = '/filter/latest?pageNumber={}&pageSize={}'
pageNumber = 0
pageSize = 20
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJlbWluLnRlcm1rcnRjaHlhbkBnbWFpbC5jb20iLCJyb2xlcyI6WyJVU0VSIl0sImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC9hcGkvbG9naW4iLCJleHAiOjE2Nzk3NzYxNDUsImlhdCI6MTY3OTc3NTU0NX0.OxWzZg8t6wDoPaOs2J-Bfim6jexEMHMNr0ohryrOsFw"
headers = {"Authorization": f"Bearer {token}"}


# In[3]:


api_path = latests
url = (url_base + api_path).format(pageNumber, pageSize)

if (api_path == profiles):
    response = requests.get(url, headers = headers)
    data = json.loads(response.text)
    content = data['content']
elif (api_path == latests):
    response = requests.get(url)
    data = json.loads(response.text)
    content = data['content']
else:
   print("NO REQUEST YET")


# In[4]:


if (api_path == profiles):
    for profile in content:
        id = profile['id']
        firstName = profile['firstName']
        lastName = profile['lastName']
        print("ID:{} - {} {}".format(id, firstName, lastName))
elif (api_path == latests):
    for watchable in content:
        id = watchable['id']
        name = watchable['name']
        rating = watchable['rating']
        print("ID:{} - {}({})".format(id, name, rating))
else:
   print("NO REQUEST YET")


# In[5]:


import pandas as pd

import sys

n_movies = int(sys.argv[-1])

genres_list = []
for i in range(1, len(sys.argv)-1):
    genres_list.append(sys.argv[i])


genres =  pd.read_json('movieAppData/genres.json')

watchable =  pd.read_json('movieAppData/watchable.json')



def recommend_according_to_genre(genre, n_movies = 7):
    genre_movies = genres[genres['genre'].isin(genre)]['watchable_id']


    watched_movies = watchable[watchable['id'].isin(genre_movies)].sort_values(by=['rating', "vote_count"], ascending=[ False,False])
    
    top_n_movies = watched_movies.head(n_movies)
    
    top_n_movies.reset_index(drop = True, inplace = True)
    
    
    result = top_n_movies["id"].to_dict()
    

    return top_n_movies 

# In[ ]:


app = Flask(__name__)

@app.route('/api/recommend')
def recommend():
    return recommend_according_to_genre()

if __name__ == '__main__':
    app.run()


# In[ ]:




