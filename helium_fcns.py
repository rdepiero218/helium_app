import requests
import pandas as pd
import numpy as np

from datetime import datetime, tzinfo
from dateutil import tz

address = '13Mbr1vbV5s7X1quVzFMpi8yZQ9a4PXwqFBYaD9zaPRSEDgaKmq'
names = {
    'mean-cotton-pike':'Silvia', 
    'little-mandarin-tortoise':'Reggie', 
    'faithful-mulberry-hawk':'Jared',
    'brisk-bone-beetle':'Jason'}

# ## Dates for testing
# start_date = '2021-12-01'
# end_date = '2021-12-26'

def get_account_hotspot_data():
    address = '13Mbr1vbV5s7X1quVzFMpi8yZQ9a4PXwqFBYaD9zaPRSEDgaKmq'
    url = 'https://api.helium.io/v1/accounts/'+ address +'/hotspots'
    r = requests.get(url=url)
    data = r.json()
    df = pd.DataFrame(data['data'])
    return df

def convert_to_local_time(utc_date):
    date = datetime.strptime(utc_date, '%Y-%m-%dT%H:%M:%S.%f%z')
    local = date.astimezone(tz.tzlocal())
    local_str = local.strftime('%m/%d/%Y %H:%M:%S')
    return local_str

def get_total_rewards(address, start_date, end_date):
    rewards_url = 'https://api.helium.io/v1/hotspots/' + address + '/rewards/sum'
    params = {'max_time': end_date ,'min_time': start_date}
    ### note: excludes block that includes max_time need to adjust for this in date entry
    r = requests.get(url=rewards_url, params=params)
    reward_data = r.json()
    coins = reward_data['data']['total']
    return coins

def add_coins_to_df(df, start_date, end_date):
    wallet = []
    s = pd.Series(df['address'])
    for index, address in s.iteritems():
        coins = get_total_rewards(address, start_date, end_date)
        wallet.append(coins)
        # print('%s earned %0.2f helium coins'%(address, coins))
    df['Coins'] = wallet
    return df

def get_coins(df, start_date, end_date):
    s = pd.Series(df['address'])
    coins = s.apply(get_total_rewards, start_date=start_date, end_date=end_date)
    return coins

def get_current_price():
    r = requests.get('https://api.helium.io/v1/oracle/prices/current')
    price = r.json()['data']['price']
    HNT = price/100000000
    return HNT

def clean_up_df(df):
    ### extract status data
    status = df['status'].apply(pd.Series)
    status = status.rename(columns={'timestamp': 'timestamp_online'})
    ### add to df
    df = pd.concat([df, status], axis=1)
    ### convert timestamps
    df['timestamp_added'] = df['timestamp_added'].apply(convert_to_local_time)
    df['timestamp_online'] = df['timestamp_online'].apply(convert_to_local_time)
    
    ### add owner names
    df['Owner'] = df['name'].map(names)
    ### move owner to front of df
    df.insert(0,'Owner', df.pop('Owner'))
    df['Amount'] = df['Amount'].round(decimals=2)
    df['Coins'] = df['Coins'].round(decimals=4)
    return df

def get_account_balance():
    address = '13Mbr1vbV5s7X1quVzFMpi8yZQ9a4PXwqFBYaD9zaPRSEDgaKmq'
    url = 'https://api.helium.io/v1/accounts/'+address
    r = requests.get(url=url)
    data = r.json()
    data = data['data']
    balance = data['balance']/100000000
    return balance