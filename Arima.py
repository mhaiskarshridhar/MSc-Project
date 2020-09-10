from statsmodels.tsa.arima_model import ARIMA
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta
import itertools
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import ast
from sklearn.metrics import mean_squared_error

def Generate_Dataframe():
    df_final=pd.DataFrame()
    all_files=[r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk3.csv',
             r'C:\Users\Mhaiskao\TikTok_Analysis\tiktok_chunk4.csv']
    df_final = pd.concat((pd.read_csv(f,index_col=0) for f in all_files))

    print(df_final['ID'][0:5])

    array=[ast.literal_eval(x) for x in df_final['Scrape_time List']]
    df_final['Scrape_time List']=array

    array=[ast.literal_eval(x) for x in df_final['Playcount List']]
    df_final['Playcount List']=array

    array=[ast.literal_eval(x) for x in df_final['Commentcount List']]
    df_final['Commentcount List']=array

    array=[ast.literal_eval(x) for x in df_final['Diggcount List']]
    df_final['Diggcount List']=array

    return df_final

def visualize_arima(output,time,mean_comment,name1,fig1,col_number):
    #save the last date and use stripftime to generate 7 days from last date
    date_time_str = time[-1]
    Predicted_Value_dates=[]

    #check if length of input was 1
    if len(mean_comment)==1:
        for i in range(1,8):
            res = (datetime.strptime(date_time_str, '%m/%d/%y %H') + timedelta(days=i)).strftime('%m/%d/%y')
            Predicted_Value_dates.append((res,output))
    else:
        for i in range(1,8):
            res = (datetime.strptime(date_time_str, '%m/%d/%y %H') + timedelta(days=i)).strftime('%m/%d/%y')
            Predicted_Value_dates.append((res,output[i-1]))

    #create data frame to plot the graphs
    df=pd.DataFrame()
    df[['Date','Predicted_Value']]=pd.DataFrame(Predicted_Value_dates)

    # Initialize figure with subplots

    fig1.add_trace(go.Scatter(x=df['Date'], y=df['Predicted_Value'], name=name1,
                             line = dict(width=2),text=df['Predicted_Value']),row=1,col=col_number)


    return


#######################################################################################################################

def arima_model(sub_string,parameter):
    parameters=[]

    arima_df=pd.DataFrame()
    Time=arima_df['time']=sub_string['Scrape_time List'][0]
    arima_df['comment']=sub_string[parameter][0]

    date_list=[]
    for i in range(0,len(arima_df['time'])):
        date_list.append(datetime.strptime(arima_df['time'][i], '%m/%d/%y %H').strftime('%m/%d/%y'))
    arima_df['time']=date_list
    mean_comment=arima_df['comment']
    mean_comment=mean_comment.diff()
    arima_df['comment']=mean_comment
    mean_comment=arima_df.groupby('time')['comment'].mean().round()

#     autocorrelation_plot(mean_comment)
#     pyplot.show()

    if len(arima_df) < 100:
        print('Not much value to train')
        return
    p=q=d=range(0,5)
    pdq=list(itertools.product(p,d,q))

    parameters=[]
    error_list=[]

    for param in pdq:
        print('p d q values ',param)
        x=1
        X = mean_comment.values
        size = int(len(X) * 0.80)
        train, test = X[0:size], X[size:len(X)]
        history = [x for x in train]
        predictions = list()
        for t in range(len(test)):
            try:
                model = ARIMA(history, order=param)
                model_fit = model.fit(disp=0)
            except:
                x=0
                break
            output = model_fit.forecast()
            yhat = output[0]

            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
            try:
                #print('predicted=%f, expected=%f' % (int(yhat), obs))
                pass
            except:
                pass
        if x==0:
            continue
        try:
            error = mean_squared_error(test, predictions)
            print(error)
            parameters.append(param)
            error_list.append(error)
        except:
            continue

    mydict2=dict(zip(parameters,error_list))
    if len(mydict2)==0:

        return visualize_arima(mean_comment[0], Time, mean_comment)
    print('Mean Squared Error',mydict2)
    Keymax = min(mydict2, key= lambda x: mydict2[x])
    print('Optimum (p,d,q) values', Keymax )
    model = ARIMA(mean_comment.values, order=Keymax)
    model_fit = model.fit(disp=0)
    output=model_fit.forecast(steps=7)[0]

    output = [round(x) for x in output]
    print(parameter,'---',output)

    return output,Time,mean_comment
#     return visualize_arima(output,Time,mean_comment1,mean_time)
##############################################################


def Predict_Values(videoid):
    df_final=Generate_Dataframe()
    df=df_final.loc[df_final['ID'] == videoid]
    df.reset_index(drop=True,inplace=True)

    fig1=go.Figure()
    fig1 = make_subplots(rows=1, cols=3)
    fig1.update_layout(yaxis_type="log")

    output,Time,mean_comment=arima_model(df,'Commentcount List')
    visualize_arima(output,Time,mean_comment,'Commentcount List',fig1,1)


    output,Time,mean_comment=arima_model(df,'Diggcount List')
    visualize_arima(output,Time,mean_comment,'Digg List',fig1,2)


    output,Time,mean_comment=arima_model(df,'Playcount List')
    visualize_arima(output,Time,mean_comment,'Playcount',fig1,3)

    fig1.show()

Predict_Values(6798117698233453829)
