import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import lxml



def priceTracker():
    url = 'https://finance.yahoo.com/quote/BTC-USD'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    #print(soup)

    price = soup.find_all('div',{'class':'container svelte-aay0dk'})[0].find('span').text
    return price

def priceTracker2():
    url = 'https://finance.yahoo.com/quote/BTC-EUR'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    #print(soup)

    price = soup.find_all('div',{'class':'container svelte-aay0dk'})[0].find('span').text
    return price

while True:
    current_time = datetime.now()
    #st.dataframe(f'Current Time: {current_time}'), print(f'BIT USA: {priceTracker()}'),print(f'BIT EUR: {priceTracker2()}')
    data = {
        'Time': [current_time],
        'Bitcoin Price (USD)': [priceTracker()],
        'Bitcoin Price (EUR)': [priceTracker2()]
    }
    st.json(data)
    time.sleep(3)

def store(dt = [currenttime,pricetracker,pricetracker2]):
    data = pd.DataFrame(dt)
    data.to_csv("data.csv")
store(dt = [current_time,priceTracker(),priceTracker2()])
