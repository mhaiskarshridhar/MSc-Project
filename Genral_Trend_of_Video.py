# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 02:04:41 2020

@author: Peaky Blinder
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ast
import pandas as pd

def Generate_Dataframe():
    df_final=pd.DataFrame()
    all_files=[r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk3.csv',r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk4.csv']
    df_final = pd.concat((pd.read_csv(f,index_col=0) for f in all_files))
    return df_final

def visualize_CMD(df_final,tiktokid):
    index=df_final.index[df_final['ID'] == tiktokid].tolist()

    scrape_time=ast.literal_eval(df_final['Scrape_time List'][index[0]])
    comment_count=ast.literal_eval(df_final['Commentcount List'][index[0]])
    share_count=ast.literal_eval(df_final['Sharecount List'][index[0]])
    play_count=ast.literal_eval(df_final['Playcount List'][index[0]])
    digg_count=ast.literal_eval(df_final['Diggcount List'][index[0]])

    # Initialize figure with subplots
    fig = make_subplots(
        rows=3, cols=2,
        column_widths=[0.9, 0.9],
        row_heights=[0.5, 0.2,0.5],
        specs=[[{"type": "Scatter"}, {"type": "Scatter"}],
               [None , None ],
               [{"type": "Scatter"}, {"type": "Scatter"}]])


    # Add Comment Count Scatter chart
    fig.add_trace(go.Scatter(x=scrape_time, y=comment_count, name='Comment Count',
                             line = dict(color='red', width=2)),row=1,col=1)

    # Add Share Count Scatter chart
    fig.add_trace(go.Scatter(x=scrape_time, y=share_count, name='Share Count',
                             line = dict(color='blue', width=2)),row=1,col=2)

    # Add Digg Count Scatter chart
    fig.add_trace(go.Scatter(x=scrape_time, y=digg_count, name='Digg Count',
                             line = dict(color='green', width=2)),row=3,col=1)

    # Add Playcount Count Scatter chart
    fig.add_trace(go.Scatter(x=scrape_time, y=play_count, name='Play Count',
                             line = dict(color='black', width=2)),row=3,col=2)

    return fig

fig=visualize_CMD(Generate_Dataframe(),6802587850870164741)
fig.show()