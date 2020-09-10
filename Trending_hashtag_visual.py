# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 04:00:07 2020

Display trending hashtags visually
@author: Peaky Blinder
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import ast

def Generate_Dataframe():
    df_final=pd.DataFrame()
    all_files=[r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk3.csv',r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk4.csv']
    df_final = pd.concat((pd.read_csv(f,index_col=0) for f in all_files))
    return df_final

def create_df_graph(df_text):
    print('in df_fraaog')
    append_list=[]
    for i in range(0,len(df_text['Author ID'])):
        for j in df_text['challenge_list_Name'][i]:
             append_list.append([df_text['Music Id'][i],df_text['Author ID'][i],j,1])
    cols = ['Music ID','Author ID','challenge_list_Name','weight']

    df_graph = pd.DataFrame(append_list,columns=cols)
    return df_graph

def unique_values(dataframe,columnname):
    print('in unique')
    dataframereturn=pd.DataFrame()
    dataframereturn=dataframe[columnname].value_counts().rename_axis('unique_values').reset_index(name='counts')
    return dataframereturn

def remove_zero_challenges(df_final):
    #Remove rows having Zero challenges
    print('in zero challenge')
    df_text=df_final[['Music Id','Author ID','challenge_list_Name','Verified List','follower_count','Created Time']]
    df_text=df_text.loc[df_text['Verified List']==True]
    df_text=df_text.dropna()
    df_text.reset_index(drop=True,inplace=True)

    array=[ast.literal_eval(x) for x in df_text['challenge_list_Name']]
    df_text['challenge_list_Name']=array
    return df_text

def Hashtag_Trend(challenges,df_final):

    for challenge in challenges:
        challenge='#' + challenge
        df_sub_string=df_final[df_final["Text"].str.contains(challenge,regex=True)]
        df_sub_string.reset_index(drop=True, inplace=True)
        df_sub_string=df_sub_string.loc[df_sub_string['Created Time'] == '03/15/20']
        df_sub_string.reset_index(drop=True, inplace=True)
        df_sub_string.sort_values("Created Time", axis = 0, ascending = False, inplace = True)
        comment_total=[]
        time_total=[]
        array=[ast.literal_eval(x) for x in df_sub_string['Diggcount List']]
        df_sub_string['Diggcount List']=array
        array=[ast.literal_eval(x) for x in df_sub_string['Bin Time']]
        df_sub_string['Bin Time']=array
        #print(df_sub_string[['Diggcount List','Bin Time']])
        for i in range(0,len(df_sub_string)):
            comment_diff=[]
            time_diff=[]
            start_value=df_sub_string['Diggcount List'][i][0]
            comment_diff.extend(np.diff(df_sub_string['Diggcount List'][i]))
            for i in df_sub_string['Bin Time'][i][1:]:
                print([i[:8]])
                time_diff.extend([i[:8]])
            mean_comment=pd.DataFrame()
            mean_comment['Time']=time_diff
            mean_comment['Comment']=comment_diff
			print(challenge)
            mean_comment=mean_comment.groupby(['Time'])['Comment'].sum()
            for i in range(0,len(mean_comment)):
                start_value=start_value + int(mean_comment[i])
                comment_total.append(start_value)
                time_total.append(mean_comment.index[i])

        mean_comment=pd.DataFrame()
        mean_comment['Time']=time_total
        mean_comment['Comment']=comment_total
        mean_comment=mean_comment.groupby(['Time'])['Comment'].mean()


        fig.add_trace(go.Scatter(x=mean_comment.index, y=mean_comment.values, name=challenge,
        line = dict( width=2)),row=1,col=1)

    return fig

df_bar_challenge=unique_values(create_df_graph(remove_zero_challenges(Generate_Dataframe())),'challenge_list_Name')
fig = make_subplots(rows=1, cols=1)
fig.update_layout(yaxis_type="log")
for i in range(3,8):
    Hashtag_Trend([df_bar_challenge['unique_values'][i]],Generate_Dataframe())
fig.show()