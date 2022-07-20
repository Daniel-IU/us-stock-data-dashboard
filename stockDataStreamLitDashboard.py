
import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_datareader import data as web
import seaborn as sns
import cufflinks as cf
import numpy as np
from datetime import datetime
cf.go_offline()

# ------------------------------------------------- Dashboard setup and data prep-------------------------------------------------

st.set_page_config(page_title='Stock data dashboard',
                     page_icon= '😂',
                     layout='wide',menu_items={
         'Get Help': 'https://www.facebook.com/',
         'Report a bug': "https://www.facebook.com/",
         'About': "# This is a header. This is an *extremely* cool app!"
     })

stocks=['AAPL','NVDA','VOO','MSFT','TSLA','GOOGL','META','AMZN','NFLX']

@st.experimental_memo()
def getData(*neededStocks):
    return web.DataReader(neededStocks,'yahoo',start='2000-01-01')['Adj Close']

stockData = getData(*stocks)

#------------------------------------------------------------Dashboard Body----------------------------------------------------------


#---------------------------------------------------------Header and images-------------------------------------------


st.title('US Stock Market Dashboard')
st.subheader('Analysis of select stock')

col1, col2 = st.columns(2)

with col1:
    st.image('StockMarket.jpg')

with col2:
    st.image('StockMarket2.jpg')
    
    
    
#-----------------------------------------------------------dashboard metrics---------------------------------------------------------


st.sidebar.markdown('# Make your selections in this sidebar')
chosenStock = st.sidebar.selectbox('For chart 1, choose a stock',['All'] + stocks)

if chosenStock == 'All':
    metricText = 'Select a stock for chart 1 to see % change'
    pctChange = 0

else:
    endDateValue = stockData[chosenStock].dropna().iloc[-1]
    startDateValue = stockData[chosenStock].dropna().iloc[0]
    startDate = stockData[stockData[chosenStock]==startDateValue].index
    startDate = startDate.strftime("%b-%Y")[0]
    pctChange = (endDateValue - startDateValue ) / startDateValue
    metricText = f'{chosenStock} % change from {startDate} till date'
    
    
col1, col2, col3 =st.columns(3)

with col1:
    st.metric('Number of stocks tracked 💰',len(stocks))

with col2:
    st.metric(metricText,f'{pctChange:,.2%}')

with col3:
    st.metric('last updated ⌚',datetime.strftime(datetime.now(),'%d/%m/%y - %H:%M'))

#-------------------------------------------------------------------chart 1 ---------------------------------------------------------------
              
st.markdown('### Chart 1: Stock price over time')

if chosenStock =='All':
    chosenStock = stocks
    
fig= px.line(stockData[chosenStock],width=850,height=400)
st.write(fig)

#------------------------------------------------------------------chart 2 ------------------------------------------------------------------

st.markdown('### Chart 2: Moving average')

chosenRollPeriod = st.sidebar.radio('For chart 2, choose a rolling period (in days)',(50,100,200,400),help='Choose a rolling period (in days)')

rolledstockData = stockData.rolling(chosenRollPeriod).mean()

fig=px.line(rolledstockData,width=850,height=400)

st.write(fig)


#---------------------------------------------------------------------Chart 3----------------------------------------------------------------

st.markdown('### Chart 3: Monthly % change')

chosenStock2 = st.sidebar.selectbox('For chart 3, choose a stock',['All']+stocks)

if chosenStock2 =='All':
    chosenStock2 = stocks


def resampleStockData():
    return stockData.resample('M').ohlc().stack(0)['close'].unstack(1).pct_change() * 100


rsd = resampleStockData()
fig=px.bar(rsd[chosenStock2],barmode='group',width=850,height=400,text_auto=True)
st.write(fig)

#---------------------------------------------------------------------junk code ---------------------------------------------------------------

#col1,col2 = st.columns(2)

#with col1:
    #st.line_chart(stockData.tail(10))
#    chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])

#    st.line_chart(chart_data,use_container_width=True)
    
#with col2:
    #st.line_chart(stockData.tail(10))
#    st.line_chart(chart_data)

#picture = st.camera_input("Take a picture")

#if picture:
#     st.image(picture)
