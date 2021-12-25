import streamlit as st
import numpy as np
import pandas as pd
import requests


st.set_page_config(page_title="Jason's Helium Empire", page_icon="💰", layout='wide')

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_url(url, link_text):
    link = f'[{link_text}]({url})'
    st.markdown(link, unsafe_allow_html=True) 

# local_css("style.css")

###--------------------
### HOTSPOT ADDRESSES
###--------------------
reggie = '112jojcx3Tcx8nvNK7q1ab3ufjkXVqkVdrpcfcyGvJzSFG4ZZmSD'
jared = '112tpR2CKvh1xXcuUM4ryQiXTSB5yWCx9r5motWJspn7iQBQzs3m'
jason = '112MNQBha2K8o8GbzpRDo1bdhubrrZxq6uG7nyhBWUrvfCm7fLm1'
silvia = '112MUF8fkkqGn5uHDhBS2XGXtFKGuQf5qqBkFJZyiukhvdid8kWi'

hotspots = {'Reggie':reggie, 'Jared':jared, 'Silvia': silvia, 'Jason':jason}
## put in a dataframe
data = pd.DataFrame.from_dict(hotspots, orient='index', columns=['Address'])

###--------------------
### FUNCTIONS
###--------------------
def get_total_rewards(address, start_date, end_date):
    rewards_url = 'https://api.helium.io/v1/hotspots/' + address + '/rewards/sum'
    params = {'max_time': end_date ,'min_time': start_date}
    ### note: excludes block that includes max_time need to adjust for this in date entry
    r = requests.get(url=rewards_url, params=params)
    reward_data = r.json()
    coins = reward_data['data']['total']
    return coins

def get_current_price():
    r = requests.get('https://api.helium.io/v1/oracle/prices/current')
    price = r.json()['data']['price']
    HNT = price/100000000
    return HNT



col1, col2 = st.columns(2)
with col1:
    st.image('./images/jason2.png', use_column_width='auto')
with col2:
    st.image('./images/helium-logo.png', use_column_width='auto')

###--------------------
st.title('Jason\'s Helium App')
###--------------------

### testing in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.header('Enter Dates 📆')

    ### ENTER START AND END DATES
    start_date = st.text_input('Enter a start date in YYYY-MM-DD format', '2021-12-01')
    # st.write('You entered the start date', start_date)

    end_date = st.text_input('Enter an end date in YYYY-MM-DD format', '2021-12-24')
    # st.write('You entered the end date', end_date)
with col2:
    st.container()

with col3: 
    wallet = []

    for hotspot in hotspots.keys():
        coins = get_total_rewards(hotspots[hotspot], start_date, end_date)
        wallet.append(coins)
        print('%s earned %0.2f helium coins'%(hotspot, coins))

    data['Coins'] = wallet

    ### get current price for HNT
    HNT = get_current_price()

    data['Amount'] = data[['Coins']] * HNT
    ###--------------------
    ### PRINT RESULTS
    ###--------------------
    st.header('Hotspot Earnings 🤑')

    st.write('Results for ', start_date, ' to ', end_date)
    st.table(data[['Coins', 'Amount']])

# ###--------------------
# st.header('Enter Dates 📆')

# ### ENTER START AND END DATES
# start_date = st.text_input('Enter a start date in YYYY-MM-DD format', '2021-12-01')
# st.write('You entered the start date', start_date)

# end_date = st.text_input('Enter an end date in YYYY-MM-DD format', '2021-12-24')
# st.write('You entered the end date', end_date)

# st.dataframe(data)


# wallet = []

# for hotspot in hotspots.keys():
#     coins = get_total_rewards(hotspots[hotspot], start_date, end_date)
#     wallet.append(coins)
#     print('%s earned %0.2f helium coins'%(hotspot, coins))

# data['Coins'] = wallet

# ### get current price for HNT
# HNT = get_current_price()

# data['Amount'] = data[['Coins']] * HNT
# ###--------------------
# ### PRINT RESULTS
# ###--------------------
# st.header('Hotspot Earnings 🤑')

# st.write('Results for ', start_date, ' to ', end_date)
# st.dataframe(data[['Coins', 'Amount']])

### 
# st.bar_chart(data[['Coins']])
# ###--------------------
st.header('Total Earnings 💰')
# ###--------------------
total_coins = round(data['Coins'].sum(), 4)
total_earned = round(data['Amount'].sum(),2)

# st.write('You have earned a total of ', total_coins, ' HNT which is equivalent to $', total_earned)
# st.write('You have earned a total of %0.2f HNT which is equivalent to $ %0.2f'%(total_coins, total_earned))


col1, col2 = st.columns(2)
with col1:
    st.metric('HNT', total_coins)
with col2:
    st.metric('USD', total_earned)


