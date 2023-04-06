#!/usr/bin/env python3

import datetime
import os
import pandas as pd
from yahoo_fin import news

# specify the ticker you want to get headlines for
ticker = input('Enter a ticker: ')

# shows you where this file is located
current_dir = os.getcwd()

# define filename
filename = f'{ticker}_news.csv'

# adds filename to path
filepath = os.path.join(current_dir, filename)

# check if the file exists in the current directory
if os.path.isfile(os.path.join(current_dir, filename)):
    print(f"{filename} EXISTS in the current dir")
else:
    print(f"{filename} DOES NOT exist in the current dir")

# get headlines into news_df
news_df = news.get_yf_rss(f"{ticker}")

# Create empty lists for titles and links
titles = []
links = []

# Loop through news items and extract title and link data
for news in news_df:
    titles.append(news['title'])
    links.append(news['link'])

# Create a DataFrame from the lists
df = pd.DataFrame({'Title': titles, 'Link': links})

# addind date column
today = datetime.datetime.today().strftime('%Y-%m-%d')
df['Date'] = today

# check if the file exists
if os.path.isfile(filepath):
    # read the existing data into a dataframe
    df2 = pd.read_csv(filepath)

    # merge the existing data with the new data
    appended_df = pd.merge(df2, df, how='outer')

    # save the appended data to the same file
    appended_df.to_csv(filepath, index=False)

    print(f"new data was added")
else:
    # save the new data to a new file with the specified filename
    df.to_csv(filepath, index=False)

    print(f"{filename} was created")

# reloading csv to handle duplicates
news = pd.read_csv(filepath)

# checking for duplicates
duplicates = news[news.duplicated(subset=['Title'])]

# Remove duplicates
news.drop_duplicates(subset=['Title'], inplace=True)

df = news
df.to_csv(filepath, index=False)
print(f"{filename} resaved sans duplicates")
