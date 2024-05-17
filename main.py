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

def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('rtd.csv', index=False)
    st.success("Data saved to CSV file successfully!")
    
def main():   
    while True:
        current_time = datetime.now()
        st.dataframe(f'Current Time: {current_time}'), print(f'BIT USA: {priceTracker()}'),print(f'BIT EUR: {priceTracker2()}')
        data = {
            'Time': [current_time],
            'Bitcoin Price (USD)': [priceTracker()],
            'Bitcoin Price (EUR)': [priceTracker2()]
        }
        st.json(data)
        save_to_csv(data)
        time.sleep(30)
        
        #if current_time.hour == 0 and current_time.minute == 0:
            #save_to_csv(data)

if __name__ == "__main__":
    main()