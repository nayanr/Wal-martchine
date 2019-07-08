#!/usr/bin/env python
# coding: utf-8

# In[14]:


import numpy
import matplotlib.pyplot as plt
import os
import sklearn


# In[15]:


import pandas as pd


# In[16]:


df = pd.read_csv('filtered.csv')


# In[17]:


df = df.iloc[:, [1 , 3]]


# In[18]:


df


# In[28]:


print(df.iloc[1 , 1])
type(df.iloc[1 , 1])


# In[31]:


n , m  = df.shape


# In[32]:


n , m


# In[33]:


ingredients_list = []
for i in range(0 , n) :
    ingredients_list.append(df.iloc[i , 1])


# jdfd
# 

# In[38]:


for i in range(0 , n):
    ingredients_list[i] = ingredients_list[i][1:-1]


# In[61]:


ingredients_list
fine = {"romaine lettuce"}
for i in range(0 , n) :
    s = ingredients_list[i] 
    l = len(s)
    flag = False
    c = ""
    for j in range(0 , l):
        if flag == False:
            if(s[j] == '\'') :
                flag = True
                continue
            else :
                continue
        if flag == True:
            if s[j] != '\'':
                c = c + str(s[j])
            else :
                flag = False
                fine.add(c)
                c = ""
    if(len(c) != 0) :
        fine.add(c)


# In[62]:


l = len(fine)
ingredients = fine
        


# In[186]:


len(ingredients)
binary = []


# In[187]:



def Convert(string): 
    li = list(string.split("-")) 
    print(li)
    add = [0] * len(ingredients);
    for ingredient in ingredients:
        i = 0
        for name in li:
            if name == ingredients:
                add[i] = 1
                break
            else :
                add[i] = 0
        i = i + 1
    binary.append(add)


# In[213]:



str = "salmon fillets-shallots-cumin seed-fresh cilantro-salt-curry powder-vegetable oil-serrano chile-fresh ginger-sauce"

print(Convert(str))

str = "coarse salt-fenugreek-urad dal-potatoes-white rice-vegetable oil"

print(Convert(str))


str = "italian seasoning-broiler-fryer chicken-mayonaise-zesty italian dressing"

print(Convert(str))

str = "stock-curry powder-cracked black pepper-minced beef-onions-plain flour-bread crumbs-butter-garlic-celery-cold water-tumeric-dried thyme-ginger-oil-tomatoes-water-paprika-salt-chillie"

print(Convert(str))

str = "black pepper-apple cider vinegar-garlic-brown sugar-jamaican jerk season-red pepper flakes-salt-olive oil-butter-purple onion-pineapple preserves-shallots-chicken drumsticks-red bell pepper"

print(Convert(str))


# In[214]:


len(binary)


# In[215]:


import random
for li in binary:
    sum = 0;
    for i in range(0 , len(li)):
        if(li[i] == 0): 
            continue
        sum = sum + li[i]
    if sum == 0:
        continue
    for i in range(0 , len(li)):
        li[i] = li[i] / sum
        


# In[216]:


1


# In[219]:


len(binary)


# In[193]:


len(ingredients)


# In[ ]:




