#!/usr/bin/env python
# coding: utf-8

# # Web Scraping 1mg

# In[1]:


import requests
from bs4 import BeautifulSoup as soup


# In[2]:


header = {'Origin': 'https://www.1mg.com',
'Referer': 'https://www.1mg.com/categories/exclusive/immunity-boosters/vitamin-c-734',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}


# In[3]:


url = 'https://www.1mg.com/categories/exclusive/immunity-boosters/vitamin-c-734'


# In[4]:


html = requests.get(url=url,headers=header)
html.status_code


# In[5]:


bsobj = soup(html.content,'lxml')
bsobj


# In[6]:


bsobj.findAll('div',{'itemprop':'name'})


# In[7]:


product_name = []
for name in bsobj.findAll('div',{'itemprop':'name'}):
    product_name.append(name.text.strip())
    
product_name


# In[8]:


len(product_name)


# In[9]:


pack_size = []

for size in bsobj.findAll('div',{'class':'style__pack-size___2JQG7'}):
    pack_size.append(size.text.strip())
    
pack_size


# In[11]:


mrp = []

for price in bsobj.findAll('div',{'class':'style__price-tag___cOxYc'}):
    mrp.append(int(price.text.replace('₹','').replace('MRP','').strip()))
    
    
mrp
    


# In[12]:


d1 = {'pname':product_name,'psize':pack_size,'mrp':mrp}


# In[13]:


import pandas as pd


# In[14]:


df = pd.DataFrame.from_dict(d1)
df

