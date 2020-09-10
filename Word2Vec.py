# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 17:26:45 2020

@author: Peaky Blinder
"""
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
import pandas as pd
warnings.filterwarnings(action = 'ignore')

import gensim
from gensim.models import Word2Vec
import re

def Generate_Dataframe():
    df_final=pd.DataFrame()
    all_files=[r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk3.csv',r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk4.csv']
    df_final = pd.concat((pd.read_csv(f,index_col=0) for f in all_files))
    return df_final

df_final=Generate_Dataframe()

df_text=pd.DataFrame()
Hashtag_list=[]
for i in range(len(df_final['Text'])):
    Hashtag=re.findall('#(\w+)', df_final['Text'][i])
    if len(Hashtag)==0:
        Hashtag_list.append('NaN')
    else:
        Hashtag_list.append(Hashtag)
df_text['Text']=Hashtag_list
# df_text['Text']=df_final.loc[:,'challenge_list_Name']
# df_text['Text']=df_final['challenge_list_Name'].loc[df_final['Author ID']=='6652121681941217285']
df_text.drop(df_text[df_text['Text'] == 'NaN'].index, inplace = True)
df_text.reset_index(inplace=True,drop=True)
df_text['Text'].head()
# Calculate frequency of each hashtag
df_Famous_Hashtag=df_text['Text'].apply(pd.Series).stack().value_counts()
df_Hashtag_Count=pd.DataFrame()
df_Hashtag_Count['Hashtag']=df_Famous_Hashtag.index
df_Hashtag_Count['Count']=df_Famous_Hashtag.values
df_Hashtag_Count.drop(df_Hashtag_Count[(df_Hashtag_Count['Hashtag'] == 'fyp') | (df_Hashtag_Count['Hashtag'] == 'foryou')
                                      | (df_Hashtag_Count['Hashtag'] == 'foryoupage')
                                      | (df_Hashtag_Count['Hashtag'] == 'foryourage')
                                      | (df_Hashtag_Count['Hashtag'] == 'foryourpage')
                                      | (df_Hashtag_Count['Hashtag'] == 'fy')].index, inplace = True)
# take hashtags which appear at least this amount of times
min_appearance = 200
# find popular hashtags - make into python set for efficiency
popular_hashtags_set = set(df_Hashtag_Count[
                           df_Hashtag_Count.Count>=min_appearance
                           ]['Hashtag'])

# make a new column with only the popular hashtags
df_text['popular_hashtags'] = df_text.Text.apply(
            lambda hashtag_list: [hashtag for hashtag in hashtag_list
                                  if hashtag in popular_hashtags_set])
# drop rows without popular hashtag
popular_hashtags_list_df = df_text.loc[
            df_text.popular_hashtags.apply(lambda hashtag_list: hashtag_list !=[])]

data=list(popular_hashtags_list_df['popular_hashtags'])

# Create Skip Gram model
model2 = gensim.models.Word2Vec(data, min_count = 1, size = 84369,
                                             window = 5, sg = 1)

print(model2.most_similar('covid19'))