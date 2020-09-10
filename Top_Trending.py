# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 01:20:58 2020
Plot Top 20 Challenges
@author: Peaky Blinder
"""

import plotly.express as px
import pandas as pd
import ast
import plotly.graph_objects as go
import plotly.figure_factory as ff
import d3fdgraph


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

def unique_values(dataframe,columnname):
    print('in unique')
    dataframereturn=pd.DataFrame()
    dataframereturn=dataframe[columnname].value_counts().rename_axis('unique_values').reset_index(name='counts')
    return dataframereturn

def visualize_top20_challenge(df_graph):
    print('in top 20')
    df_bar_challenge=unique_values(df_graph,'challenge_list_Name')
    fig = px.bar(df_bar_challenge[0:20], x='counts', y='unique_values',
				 text='counts',orientation='h', title='Top 20 Challenges')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    return fig

def visualize_top20_MusicName(df_final):
    #Unique values for Music Names
    df_bar_music_name=unique_values(df_final,'Music Name')
    #Skipped 1st music name since random orignal music is represented as 'orginal music'.
    # Thus the category 'orginal music' represent multiple songs
    fig = px.bar(df_bar_music_name[1:20], x='counts', y='unique_values',
				 text='counts',orientation='h', title='Top 20 Music Names')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    return fig


def visualize_top20_MusicID(df_final):
    # #Unique values for Music Ids
    df_bar_music_id=unique_values(df_final,'Music Id')
    index=list(range(10))
    music_id = list(df_bar_music_id['unique_values'][0:10])
    counts = list(df_bar_music_id['counts'][0:10])
    Table=[]
    Table.append(['Index','Music Id','Count'])
    for  i in range(0,len(music_id)):
        Table.append([i,music_id[i],counts[i]])
    fig = ff.create_table(Table, height_constant=60)
    Music_Bar = go.Bar(x=index, y=counts, xaxis='x2', yaxis='y2',
                    marker=dict(color='#0099ff'),
                    name='Count')
    print(Table[:20])
    fig.add_traces(Music_Bar)
    # initialize xaxis2 and yaxis2
    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}
    # Edit layout for subplots
    fig.layout.xaxis.update({'domain': [0, .5]})
    fig.layout.xaxis2.update({'domain': [0.6, 1.]})
    # The graph's yaxis MUST BE anchored to the graph's xaxis
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.yaxis2.update({'title': 'Count'})
    fig.layout.xaxis2.update({'title': 'index'})
    fig.layout.margin.update({'t':75, 'l':50})
    fig.layout.update({'title': 'Trending Music on TikTok'})
    return fig


def visualize_hashtag_for_music(df_graph,musicid):
    listauthor=df_graph.index[df_graph['Music ID'] == musicid].tolist()
    cols = ['source','target','weight']
    list_directed_graph=[]
    #Create list having format Music Id : challenge1;
    for i in listauthor:
        list_directed_graph.append([df_graph['Music ID'][i],df_graph['challenge_list_Name'][i],5])

    df_directed_graph=pd.DataFrame(list_directed_graph,columns=cols)
    d3fdgraph.plot_force_directed_graph(df_directed_graph, node_radius=15, link_distance=30, collision_scale=4)

visualize_hashtag_for_music(create_df_graph(remove_zero_challenges(Generate_Dataframe())),'6735137560026172166')

fig=visualize_top20_MusicID(Generate_Dataframe())
fig.show()

fig=visualize_top20_MusicName(Generate_Dataframe())
fig.show()

fig=visualize_top20_challenge(create_df_graph(remove_zero_challenges(Generate_Dataframe())))
fig.show()