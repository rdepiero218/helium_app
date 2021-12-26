import streamlit as st
import numpy as np
import pandas as pd
import requests

import helium_fcns as h

import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Jason's Helium Empire", page_icon="💰", layout='wide')


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_url(url, link_text):
    link = f'[{link_text}]({url})'
    st.markdown(link, unsafe_allow_html=True) 

local_css("style.css")


###-------------------------------------
col1, col2 = st.columns(2)
with col1:
    st.image('./images/jason2.png', use_column_width='auto')
with col2:
    st.image('./images/helium-logo.png', use_column_width='auto')

###--------------------
st.title('Jason\'s Helium Empire')
###--------------------


### GET HOTSPOT ADDRESSES
df = h.get_account_hotspot_data()

###--------------------
st.header('Enter Dates 📆')
###--------------------
### ENTER START AND END DATES
start_date = st.text_input('Enter a start date in YYYY-MM-DD format', '2021-12-01')
# st.write('You entered the start date', start_date)
end_date = st.text_input('Enter an end date in YYYY-MM-DD format', '2021-12-24')
# st.write('You entered the end date', end_date)

### GET COINS
df['Coins'] = h.get_coins(df,start_date, end_date)

### USD value of coins
HNT = h.get_current_price()
df['Amount'] = df[['Coins']] * HNT

dfc = h.clean_up_df(df)

###--------------------
st.header('Hotspot Earnings 🤑')
###--------------------
### PRINT RESULTS
st.write('Results for ', start_date, ' to ', end_date)
st.table(dfc[['Owner', 'name', 'Coins', 'Amount']])

### 
# st.bar_chart(data[['Coins']])
# # ###--------------------
# st.header('Total Earnings 💰')
# # ###--------------------
total_coins = round(dfc['Coins'].sum(), 4)
total_earned = round(dfc['Amount'].sum(),2)
ytd_coins = h.get_account_balance()
ytd_USD = ytd_coins * HNT
# st.write('You have earned a total of ', total_coins, ' HNT which is equivalent to $', total_earned)
# st.write('You have earned a total of %0.2f HNT which is equivalent to $ %0.2f'%(total_coins, total_earned))

# col1, col2 = st.columns(2)
# with col1:
#     st.metric('HNT', total_coins)
# with col2:
#     st.metric('USD', total_earned)

# # ###--------------------
# st.header('YTD Earnings 💰')
# # ###--------------------
# col1, col2 = st.columns(2)
# with col1:
#     st.metric('HNT', round(ytd_coins,4))
# with col2:
#     st.metric('USD', round(ytd_USD,2))

col1, col2 = st.columns(2)
with col1:
    st.header('Total Earnings 💰')
    st.metric('HNT', total_coins)
    st.metric('USD', total_earned)
with col2:
    st.header('YTD Earnings 💰')
    st.metric('HNT', round(ytd_coins,4))    
    st.metric('USD', round(ytd_USD,2))


max_idx = dfc['Amount'].idxmax()
top_earner = dfc.at[2,'Owner']
st.subheader('The top earner for this period was %s 🎉'%(top_earner))


###--------------------
st.header('Current Status ⏱')
###--------------------
st.table(dfc[['Owner', 'name', 'online','reward_scale', 'gain', 'elevation']])
# c = st.container()
# with c:
#     st.header('Testing Tables with Plotly')

#     # fig = go.Figure(data=go.Table(header, cells))
#     # fig = go.Figure(data=[go.Table(
#     # header=dict(values=['A Scores', 'B Scores'],
#     #             line_color='darkslategray',
#     #             fill_color='lightskyblue',
#     #             align='left'),
#     # cells=dict(values=[[100, 90, 80, 90], # 1st column
#     #                    [95, 85, 75, 95]], # 2nd column
#     #            line_color='darkslategray',
#     #            fill_color='lightcyan',
#     #            align='left'))
#     # ])

#     fig = go.Figure(data=[go.Table(
#         columnwidth = [80,120,80,80],
#         header=dict(values=list(['Owner', 'name', 'Coins', 'Amount']),
#                     fill_color='black',
#                     align='left'),
#         cells=dict(values=[dfc.Owner, dfc.name, dfc.Coins, dfc.Amount],
#                 fill_color='black',
#                 align='left'))
#     ])

#     # fig.update_layout(width=500, height=300)
#     st.write(fig)