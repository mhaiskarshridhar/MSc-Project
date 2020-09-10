# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 00:33:21 2020

@author: Peaky Blinder
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 21:32:23 2020

The function resturns associated challenges using data mining
@author: Peaky Blinder
"""

import pandas as pd
import re

def Generate_Dataframe():
    df_final=pd.DataFrame()
    all_files=[r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk3.csv',r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk4.csv']
    df_final = pd.concat((pd.read_csv(f,index_col=0) for f in all_files))
    return df_final

def Hashtags_associated(hashtag_name):
    df_final1=Generate_Dataframe()
    Hashtag_list=[]
    for i in range(len(df_final1['Text'])):
        hashtag=re.findall('#(\w+)', df_final1['Text'][i])
        if len(hashtag)==0:
            Hashtag_list.append('NaN')
        else:
            Hashtag_list.append(hashtag)
    df_final1['Text']=Hashtag_list
    df_hashtag=df_final1.dropna()
    df_hashtag.reset_index(drop=True,inplace=True)

    mask = [hashtag_name in x for x in df_hashtag['Text']]
    df_hashtag=df_hashtag[mask]
    df_hashtag.reset_index(drop=True,inplace=True)
    challenge_dict={}
    for i in range(0,len(df_hashtag)):
        hashtag_list=df_hashtag['Text'][i]
        for j in hashtag_list:
            if j in challenge_dict:
                challenge_dict[j]=challenge_dict[j]+1
            else:
                challenge_dict.update({j:1})
    challenge_dict=sorted(challenge_dict.items(), key=lambda x: x[1], reverse=True)
    return challenge_dict

challenge_dict=Hashtags_associated('outdoors')
df_hashtag=pd.DataFrame(challenge_dict,columns=['Hashtag','Associated Count'])
print(df_hashtag)
challenge_list=[]
for i in range(20):
    challenge_list.append(challenge_dict[i][0])
print(challenge_list)