# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 18:25:49 2020

@author: Peaky Blinder

The file lists videos which contain with specific hashtags and recommends Influencers
for those hashtags

"""
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import numpy as np

def Generate_Dataframe():
    df_final=pd.DataFrame()
    all_files=[r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk3.csv',r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk4.csv']
    df_final = pd.concat((pd.read_csv(f,index_col=0) for f in all_files))
    df_final.drop(df_final[(df_final['Final Digg Count'] >df_final['Final Play Count']) |
                      (df_final['Final Comment Count'] >df_final['Final Play Count'])
                      ].index, inplace=True)
    df_final.reset_index(inplace=True,drop=True)
    return df_final

def Calculate_Engagement_rate(df_sub_string,authorid):
    rslt_df = df_sub_string.loc[df_sub_string['Author ID'] == authorid]
    rslt_df.reset_index(inplace=True,drop=True)
    rslt_df.sort_values("Created Time", axis = 0, ascending = False, inplace = True)

    if len(rslt_df) > 10:
        rslt_df=rslt_df[:10]
    #Calculate enagament rate using formular ER=[(sharecount + diggcount + commentcount)/playcount] * 100
    Numerator=rslt_df['Final Share Count'] + rslt_df['Final Comment Count'] + rslt_df['Final Digg Count']
    Numerator_value=sum(np.array(Numerator))
    Denominator=rslt_df['Final Play Count']
    Denominator_value=sum(np.array(Denominator))
    if Numerator_value==0 or Denominator_value==0:
        return 0
    Engagement_rate= (Numerator_value/Denominator_value)*100
    return Engagement_rate
'''
def Calculate_Engagement_rate(df_sub_string,authorid):
    rslt_df = df_sub_string.loc[df_sub_string['Author ID'] == authorid]
    rslt_df.reset_index(inplace=True,drop=True)
    if len(rslt_df) > 10:
        rslt_df=rslt_df[:10]
    #Calculate enagament rate using formular ER=[(sharecount + diggcount + commentcount)/playcount] * 100
    Numerator=rslt_df['Final Share Count'] + rslt_df['Final Comment Count'] + rslt_df['Final Digg Count']
    Numerator_value=sum(np.array(Numerator))
    Denominator=rslt_df['Final Play Count']
    Denominator_value=sum(np.array(Denominator))
    if Numerator_value==0 or Denominator_value==0:
        return 0
    Engagement_rate= (Numerator_value/Denominator_value)*100
    return Engagement_rate
'''
def hashtag_df(sub):
# creating and passsing series to new column
    df_final=Generate_Dataframe()
    df_sub_string=df_final[df_final["Text"].str.contains(sub,regex=True)]
    df_sub_string.reset_index(inplace=True,drop=True)

    return(df_sub_string)

def recommend_hashtag_influencers():
    df_final=Generate_Dataframe()
    #Outdoor_hashtag=['cider']
    Outdoor_hashtag=['outdoors','nature','adventure','photography','hiking','travel']
    Author_list=[]
    Video_list=[]
    Create_time_list=[]
    for hashtag in Outdoor_hashtag:
        df_sub_string=hashtag_df('#'+hashtag.lower())
        df_sub_string.reset_index(drop=True,inplace=True)

        for i in range(0,len(df_sub_string)):
            if df_sub_string['ID'][i] in Video_list:
                Video_list.append(df_sub_string['ID'][i])
                Create_time_list.append(df_sub_string['Created Time'][i])
                #continue
            else:
                Author_list.append(df_sub_string['Author ID'][i])
                Video_list.append(df_sub_string['ID'][i])
                Create_time_list.append(df_sub_string['Created Time'][i])

    my_count = pd.Series(Author_list).value_counts()
    my_count_video_list = pd.Series(Video_list).value_counts()
    if len(my_count) > 10:
        count=10
    else:
        count=len(my_count)

    Author_Engagement_rate=[]
    for i in range(0,count):
        Author_Engagement_rate.append((my_count.index[i],Calculate_Engagement_rate(df_final,my_count.index[i])))
    return Author_Engagement_rate,my_count_video_list[:10]

Author_Engagement_rate,my_count_video_list=recommend_hashtag_influencers()

df_Author_Rate = pd.DataFrame(Author_Engagement_rate, columns=['Authod ID', 'Engagement Rate'])
df_Author_Rate=df_Author_Rate.sort_values('Engagement Rate', ascending=False)
df_Video_Rate = pd.DataFrame(columns=['Video ID','Count'])
df_Video_Rate['Video ID']=my_count_video_list.index
df_Video_Rate['Count']=my_count_video_list.values
print(df_Author_Rate)




