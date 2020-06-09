#!/usr/bin/env python
# coding: utf-8

# In[1]:


accesstoken="1264655095599333377-WJQOcVvZKOvErPE9pMZWnHGKM9nvB4"
accesstokensecret="LslqOR2YpWHguCKWSLSgrSBy2oUzCkgDGVpzVzYD7QBda"
apikey="2sDnAeAWPVPNXLCDUTNwrSL26"
apisecretkey="5WgUSKRGAumKTuccwPgUNVUruSpTMyP75AzbFJ5cYz4Mh82v5X"


# In[2]:


import tweepy as tw


# In[3]:


auth = tw.OAuthHandler(apikey, apisecretkey)
auth.set_access_token(accesstoken, accesstokensecret)
api = tw.API(auth, wait_on_rate_limit=True)


# In[4]:


from datetime import date


# In[5]:


#search=input("Enter hastag to be searched :")
#b = '"' + search + '"'
search_words = "#donaldtrump"
date_since = "2020-06-09"


# In[6]:


tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(200)


# In[7]:


tweet_details = [[tweet.geo, tweet.text,tweet.user.screen_name, tweet.user.location] for tweet in tweets]


# In[8]:


import pandas as pd

tweet_df = pd.DataFrame(data=tweet_details, columns=['geo','text','user', "location"])
pd.set_option('max_colwidth', 800)

tweet_df.head(20)


# In[9]:


tweet_df.shape


# In[10]:


tweet_df.isna().sum()


# In[11]:


tweet_df.isnull().sum()


# In[12]:


tweet_df.shape


# In[13]:


import numpy as np
tweet_df.location.replace('', np.nan, inplace=True)
tweet_df.head()


# In[14]:


tweet_df.isnull().sum()


# In[15]:


tweet_df = tweet_df[tweet_df['location'].notna()]
tweet_df.shape


# In[16]:


import re
def clean_tweets(text):
    text = re.sub("RT @[\w]*:","",text)
    text = re.sub("@[\w]*","",text)
    text = re.sub("https?://[A-Za-z0-9./]*","",text)
    text = re.sub("\n","",text)
    text = re.sub(r'[^\x00-\x7F]','', text)
    return text


# In[17]:


tweet_df['text']=tweet_df['text'].apply(lambda x: clean_tweets(x))
tweet_df['location']=tweet_df['location'].apply(lambda x: clean_tweets(x))


# In[18]:


tweet_df.head(20)


# In[19]:


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my-application")

location = geolocator.geocode("House of Commons, London")
type(location)



# In[20]:


x = input('Enter the country :')
location = geolocator.geocode(x)
a=location.latitude
b=location.longitude


# In[21]:


locations =list(tweet_df.location)


# In[22]:


from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
tweet_df['address'] = tweet_df['location'].apply(geocode,timeout=10)

tweet_df['point'] = tweet_df['address'].apply(lambda loc: tuple(loc.point) if loc else None)
    


# In[23]:


tweet_df


# In[24]:


tweet_df = tweet_df[tweet_df['point'].notna()]


# In[25]:


df=pd.DataFrame(tweet_df.point.tolist(),index=tweet_df.index,columns=['lat','long','null'])
tweet_df.drop(['geo','point'],axis=1)
df.drop(['null'],axis=1)


# In[26]:


tweets_df= pd.concat([tweet_df,df], axis=1)


# In[27]:


tweets_df


# In[28]:


tweets_df = tweets_df[tweets_df['lat'].notna()]


# In[29]:


import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster


# In[ ]:





# In[30]:


map = folium.Map(location=[a, b], zoom_start=5)
icon_url = 'https://help.twitter.com/content/dam/help-twitter/twitter-logo.png'
#icon = folium.features.CustomIcon(icon_url,icon_size=(28, 30))


# In[31]:


for idx, row in tweets_df.iterrows():
    icon_url = 'https://help.twitter.com/content/dam/help-twitter/twitter-logo.png'
    icon = folium.features.CustomIcon(icon_url,icon_size=(28, 30))
    Marker([row['lat'], row['long']],popup=row['text'],icon=icon).add_to(map)
    
map



# In[33]:


map.save('Tweet-Map.html')


# In[35]:


import dash
#from jobs import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go


# In[42]:


app = dash.Dash()


# In[45]:


app.layout=html.Div([
    html.H1('Visualizing tweets by location'),
    html.Iframe(id='map',srcDoc=open('Tweet-Map.html','r').read(),width='100%',height='600')
])


# In[44]:


if __name__ == '__main__':
    #app.run_server(debug=True)


# In[ ]:





# In[ ]:




