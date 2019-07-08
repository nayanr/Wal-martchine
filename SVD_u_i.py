#!/usr/bin/env python
# coding: utf-8

# In[78]:


import csv


# In[79]:


import pandas as pd


# In[80]:


import numpy as np


# In[106]:


u_i = pd.read_csv("u_i.csv")


# In[107]:


u_i = u_i.set_index(["user_id"])


# In[108]:


u_i = u_i.drop(columns=['Unnamed'])


# In[ ]:





# In[110]:


u, sig, v_transposed = np.linalg.svd(u_i, full_matrices=False)


# In[ ]:





# In[113]:





# In[123]:


sum_sig_90 = sum(sig)*0.9


# 

# In[124]:


sum_sig_90


# In[125]:


for i in range(len(sig)):
    sum_sig_90 = sum_sig_90 - sig[i]
    if(sum_sig_90<=0):
        j = i
        break


# In[158]:


sig_new = sig[:j]
sig_new.shape


# In[156]:


u.shape


# In[154]:


u_refined = u[:,:j]


# In[155]:


u_refined.shape


# In[143]:


v_t_refined = v_transposed[:j]


# In[145]:


v_t_refined.shape


# In[160]:


u_i_SVD = np.dot(u_refined, np.dot(np.diag(sig_new), v_t_refined))


# In[161]:


u_i_SVD.shape


# In[162]:


u_i_SVD.to_csv("u_i_SVD")


# In[169]:


u_i_SVD


# In[170]:


np.savetxt("u_i_SVD.csv", u_i_SVD, delimiter=",")


# In[ ]:




