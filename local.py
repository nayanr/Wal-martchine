# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 01:16:23 2019

@author: n0r00te
"""

import json
import pandas as pd
with open('train.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)


ingredientlist = []
list1 = []
for i,row in df.iterrows():
    list_1 = row['ingredients']
    print(list_1)
    for item in list_1:
        
        if(item in ingredientlist):
            
            continue
        else:
            
            ingredientlist.append(item)
            
len(ingredientlist)

##no. of items we will have on our grocery webpage== 6714

##creating meal-ingredient matrix,binary form





chosenCuisine = ["indian", "italian", "mexican","chinese","korean","spanish","greek","british","jamaican"]
data = df.loc[df["cuisine"].isin(chosenCuisine)]


data = data.head(1000)

data.to_csv("filtered.csv")
ingredientlist = []
list1 = []

column_list = ['dish_id']
for i,row in data.iterrows():
    list_1 = row['ingredients']
    print(list_1)
    for item in list_1:
        
        if(item in ingredientlist):
            
            continue
        else:
            column_list.append(item)
            ingredientlist.append(item)
            
len(ingredientlist)


print(ingredientlist)




###########dish ingredient table
d_i = pd.DataFrame(columns = column_list)
for i,row in data.iterrows():
       array = []
       array.append(row['id'])
       list_1 = row['ingredients']
       print(i)
       for item in ingredientlist:
           if(item in list_1):
               
               array.append(1)
           else:

               array.append(0)
       row=pd.Series(array,column_list)
       row
       d_i = d_i.append([row],ignore_index=True)
#       d_i = d_i.append(pd.DataFrame(array, columns=column_list),ignore_index=True)
       
d_i.to_csv("d_i.csv")   
len(array) 


chosenCuisine = ["indian", "italian", "mexican","chinese","korean","spanish","greek","british","jamaican"]
indian = []
italian = []
mexican = []
chinese = []
korean = []
spanish = []
greek = []
british = []
jamaican = []  

for i,row in data.iterrows():
  list_1 = row['ingredients']
  cuis = row['cuisine']
  for items in list_1:
      if(cuis == "indian"):
          indian.append(items)
      if(cuis == "italian"):
          italian.append(items)    
      if(cuis == "mexican"):
          mexican.append(items)
      if(cuis == "chinese"):
          chinese.append(items)
      if(cuis == "korean"):
          korean.append(items) 
      if(cuis == "greek"):
          greek.append(items)    
      if(cuis == "british"):
          british.append(items)    
      if(cuis == "jamaican"):
          jamaican.append(items)    
      if(cuis == "spanish"):
          spanish.append(items)    


name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']

prefer = ["indian","indian","indian","mexican","italian","italian","mexican","korean","british","jamaican","korean","spanish","greek","italian", "mexican","chinese","korean","spanish", "italian", "mexican"]
len(prefer) 

import random

u_i = pd.DataFrame(columns = column_list)
for item in range(len(name)):
       array = []
       array.append(name[item])
       preference = prefer[item]
       
       for item_1 in ingredientlist:
           
           
          if(preference == "indian"):
              if(item_1 in indian):
               
               array.append(random.choice([0,1,2,3,4,5]))
              else:

               array.append(0)
          if(preference == "italian"):
              if(item_1 in italian):
               
               array.append(random.choice([0,1,2,3,4,5]))
              else:

               array.append(0)                
          if(preference == "mexican"):
              if(item_1 in mexican):
               
               array.append(random.choice([0,1,2,3,4,5]))
              else:

               array.append(0)              
          if(preference == "chinese"):
              if(item_1 in chinese):
               
               array.append(random.choice([0,1,2,3,4,5]))
              else:

               array.append(0)           
          if(preference == "korean"):
              if(item_1 in korean):
               
               array.append(random.choice([0,1,2,3,4,5]))
              else:

               array.append(0)              
          if(preference == "greek"):
              if(item_1 in greek):
               
               array.append(random.choice([0,1,2,3,4,5]))
              else:

               array.append(0)              
          if(preference == "british"):
              if(item_1 in british):
               
               array.append(random.choice([0,1,2,3,4,5]))
              else:

               array.append(0)                 
          if(preference == "jamaican"):
              if(item_1 in jamaican):
               
               array.append(random.choice([0,1,2,3,4,5]))
              else:

               array.append(0)              
          if(preference == "spanish"):
              if(item_1 in spanish):
               
               array.append(random.choice([0,1,2,3,4,5]))
              else:

               array.append(0)             
           
       row=pd.Series(array,column_list)
       u_i = u_i.append([row],ignore_index=True)

u_i.to_csv("u_i.csv")

 ingredientlist        