# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 21:32:23 2020

The function resturns associated challenges using data mining
@author: Peaky Blinder
"""

import ast
import pandas as pd

def Generate_Dataframe():
    df_final=pd.DataFrame()
    all_files=[r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk3.csv',r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk4.csv']
    df_final = pd.concat((pd.read_csv(f,index_col=0) for f in all_files))
    return df_final

def Challenges_associated(challenge_name):
    df_final=Generate_Dataframe()
    df_challenges=df_final.dropna()
    df_challenges.reset_index(drop=True,inplace=True)

    array=[ast.literal_eval(x) for x in df_challenges['challenge_list_Name']]
    df_challenges['challenge_list_Name']=array

    mask = [challenge_name in x for x in df_challenges['challenge_list_Name']]
    df_challenges=df_challenges[mask]
    df_challenges.reset_index(drop=True,inplace=True)
    challenge_dict={}
    for i in range(0,len(df_challenges)):
        challenge_list=df_challenges['challenge_list_Name'][i]
        for j in challenge_list:
            if j in challenge_dict:
                challenge_dict[j]=challenge_dict[j]+1
            else:
                challenge_dict.update({j:1})
    challenge_dict=sorted(challenge_dict.items(), key=lambda x: x[1], reverse=True)
    return challenge_dict

challenge_dict=Challenges_associated('outdoor')
df_Challenges=pd.DataFrame(challenge_dict,columns=['Hashtag','Associated Count'])
print(df_Challenges)