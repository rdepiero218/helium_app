import streamlit as st
import numpy as np
import pandas as pd
import requests
import datetime
from datetime import timedelta

import helium_fcns as h

# import plotly.express as px
# import plotly.graph_objects as go

st.set_page_config(page_title="Jason's Helium Empire", page_icon="💰", layout='wide')


# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# def display_url(url, link_text):
#     link = f'[{link_text}]({url})'
#     st.markdown(link, unsafe_allow_html=True) 

# local_css("style.css")


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
st.header('Enter Dates 📆') ### ENTER START AND END DATES
###--------------------
st.write('Select start and end dates for the desired period')

### SELECT START DATE
start_date_entry = st.date_input(
     'Select a start date',
     datetime.date(2022, 1, 1))

start_date = start_date_entry.strftime('%Y-%m-%d')



### SELECT END DATE
end_date_entry = st.date_input(
     'Select an end date',
     datetime.date(2022, 1, 2))

### helium api excludes the end date from the result, adding day here
delta = timedelta(days=1)
end_date_corrected = end_date_entry + delta
end_date = end_date_corrected.strftime('%Y-%m-%d')

### FORMAT DATES FOR PRINTING
print_start_date = start_date_entry.strftime('%B %d, %Y')
print_end_date = end_date_entry.strftime('%B %d, %Y')

### for checking input
# st.write('You entered the end date', end_date)

### GET COINS for each hotspot
df['Coins'] = h.get_coins(df,start_date, end_date)

### Calculate USD value of coins
HNT = h.get_current_price()
df['Amount'] = df[['Coins']] * HNT

### clean up hotspot dataframe
dfc = h.clean_up_df(df)

###--------------------
st.header('Hotspot Earnings 🤑')
###--------------------
### PRINT RESULTS
st.write(print_start_date, ' to ', print_end_date)
st.table(dfc[['Owner', 'name', 'Coins', 'Amount']])

### FIND MAX EARNER FOR PERIOD
max_idx = dfc['Amount'].idxmax()
top_earner = dfc.at[max_idx,'Owner']
st.subheader('The top earner for this period was %s 🎉'%(top_earner))

###--------------------
### TOTAL EARNINGS
###--------------------

### CALCULATE TOTAL COINS THIS PERIOD
total_coins = round(dfc['Coins'].sum(), 4)
total_earned = round(dfc['Amount'].sum(),2)

### CALCULATE YTD TOTAL COINS
ytd_coins = h.get_account_balance()
ytd_USD = ytd_coins * HNT
today = datetime.date.today()
print_today = today.strftime('%B %d, %Y')

### DISPLAY TOTAL EARNINGS RESULTS
col1, col2 = st.columns(2)
with col1:
    st.header('Account Earnings', )
    st.write('%s to %s'%(print_start_date, print_end_date))
    # st.write('For ', start_date, ' to ', end_date)
    st.metric('HNT', total_coins)
    st.metric('USD', total_earned)
with col2:
    st.header('Total YTD Earnings 💰')
    st.write('November 10, 2021 to %s'%(print_today))
    st.metric('HNT', round(ytd_coins,4))    
    st.metric('USD', round(ytd_USD,2))

st.subheader('Current price of HNT: $ %0.2f'%(HNT))




###--------------------
st.header('Current Status ⏱')
###--------------------
st.table(dfc[['Owner', 'name', 'online','reward_scale','timestamp_added', 'gain', 'elevation']])
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