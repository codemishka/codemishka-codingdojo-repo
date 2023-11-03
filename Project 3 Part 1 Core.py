#!/usr/bin/env python
# coding: utf-8

# In[12]:


basics_url="https://datasets.imdbws.com/title.basics.tsv.gz"
akas_url="https://datasets.imdbws.com/title.akas.tsv.gz"
ratings_url="https://datasets.imdbws.com/title.ratings.tsv.gz"


# In[16]:


import pandas as pd
import numpy as np


# In[17]:


basics = pd.read_csv(basics_url, sep='\t', low_memory=False)
akas=pd.read_csv(akas_url, sep='\t', low_memory=False)
ratings=pd.read_csv(ratings_url, sep='\t', low_memory=False)


# In[19]:


print(basics.head())


# In[22]:


basics.replace({'\\N': np.nan}, inplace=True)


# In[23]:


basics = basics.dropna(subset=['runtimeMinutes'])


# In[24]:


basics = basics.dropna(subset=['genres'])


# In[25]:


basics = basics[basics['titleType'] == 'movie']


# In[27]:


# Keep records with startYear between 2000 and 2022
basics['startYear'] = basics['startYear'].astype(float)  # Convert to float or int if there are decimal values
basics = basics[(basics['startYear'] >= 2000) & (basics['startYear'] <= 2022)]


# In[28]:


basics = basics[~basics['genres'].str.contains("Documentary")]


# In[29]:


us_movies = akas[akas['region'] == 'US']['titleId']
basics = basics[basics['tconst'].isin(us_movies)]


# In[30]:


us_movies_akas = akas[akas['region'] == 'US']


# In[32]:


us_movies_akas = akas[akas['region'] == 'US'].copy()
us_movies_akas.replace({'\\N': np.nan}, inplace=True)


# In[33]:


ratings.replace({'\\N': np.nan}, inplace=True)


# In[34]:


us_ratings = ratings[ratings['tconst'].isin(us_movies_akas['titleId'])]


# In[38]:


# Exclude movies that are included in the documentary category.
is_documentary = basics['genres'].str.contains('documentary',case=False)
basics = basics[~is_documentary]




# In[39]:


# Filter the basics table down to only include the US by using the filter akas dataframe
keepers =basics['tconst'].isin(akas['titleId'])
keepers



# In[41]:


basics = basics[keepers]
basics


# In[ ]:


#Filtering one dataframe based on another


# In[42]:


import os



# In[43]:


data_folder = 'Data'
os.makedirs(data_folder, exist_ok=True)


# In[44]:


# Save 'basics' DataFrame to a CSV file
basics.to_csv(os.path.join(data_folder, 'basics.csv'), index=False)

# Save 'us_movies_akas' DataFrame to a CSV file
us_movies_akas.to_csv(os.path.join(data_folder, 'us_movies_akas.csv'), index=False)

# Save 'us_ratings' DataFrame to a CSV file
us_ratings.to_csv(os.path.join(data_folder, 'us_ratings.csv'), index=False)


# In[45]:


current_directory = os.getcwd()
print(current_directory)


# In[47]:


# Save 'basics' DataFrame as a compressed .csv.gz file
basics.to_csv(os.path.join(data_folder, 'basics.csv.gz'), index=False, compression="gzip")

# Save 'us_movies_akas' DataFrame as a compressed .csv.gz file
us_movies_akas.to_csv(os.path.join(data_folder, 'us_movies_akas.csv.gz'), index=False, compression="gzip")

# Save 'us_ratings' DataFrame as a compressed .csv.gz file
us_ratings.to_csv(os.path.join(data_folder, 'us_ratings.csv.gz'), index=False, compression="gzip")



# In[48]:


# Replace the original DataFrames by reading the saved files
basics = pd.read_csv(os.path.join(data_folder, 'basics.csv.gz'), compression="gzip")
us_movies_akas = pd.read_csv(os.path.join(data_folder, 'us_movies_akas.csv.gz'), compression="gzip")
us_ratings = pd.read_csv(os.path.join(data_folder, 'us_ratings.csv.gz'), compression="gzip")

# Confirm that the data is correct
print(basics.head())  # Replace 'basics' with the DataFrame you want to confirm
print(us_movies_akas.head())  # Replace 'us_movies_akas' with the DataFrame you want to confirm
print(us_ratings.head())  # Replace 'us_ratings' with the DataFrame you want to confirm


# In[ ]:




