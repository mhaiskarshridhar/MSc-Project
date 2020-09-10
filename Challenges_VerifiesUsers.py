# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 21:33:42 2020
The code displays
@author: Peaky Blinder
"""
import pandas as pd

def Generate_Dataframe():
    df_final=pd.DataFrame()
    all_files=[r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk3.csv',r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk4.csv']
    df_final = pd.concat((pd.read_csv(f,index_col=0) for f in all_files))
    return df_final

def Verified_Users_challenges():

    df_final=Generate_Dataframe()

    df_text=df_final[['Music Id','Author ID','challenge_list_Name','Verified List',
					  'follower_count','Updated Time']]
    df_text=df_text.loc[df_text['Verified List']==True]

    df_text=df_text.dropna()
    df_text.reset_index(drop=True,inplace=True)

    df_text=df_text.sort_values('follower_count',ascending=False)
    gk = df_text.groupby('Author ID')

    unique_sorted_id=df_text['Author ID'].unique()

    return unique_sorted_id,gk

unique_sorted_id,gk=Verified_Users_challenges()

for i in range(0,5):
    df_text1=gk.get_group(unique_sorted_id[i])
    print(df_text1[['Author ID','challenge_list_Name','Updated Time']][:5])
