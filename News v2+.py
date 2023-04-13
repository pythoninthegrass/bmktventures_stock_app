import datetime
import pandas as pd
from yahoo_fin import news
from pathlib import Path
import os


ticker = input('Enter a ticker: ')

# get the directory of the Python file
current_dir = Path().resolve()
# print(current_dir)

# check to see if there's an existing news file for this company

# define filename
filename = f'{ticker}_news.csv'

# adds filename to path
filepath = current_dir / filename

# print(filepath)

# check if the file exists in the current directory
if filepath.is_file():
    print(f"{filename} EXISTS in the current dir")
else:
    print(f"{filename} DOES NOT exist in the current dir")
    
    
# get headlines into news_df
news_df = news.get_yf_rss(f"{ticker}")

# putting titles and links into df

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


if filepath.is_file():
    # read the existing data into a dataframe
    df2 = pd.read_csv(filepath)

    # merge the existing data with the new data
    appended_df = pd.merge(df2, df, how='outer')

    # save the appended data to the same file
    appended_df.to_csv(filepath, index=False)

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

# count the number of rows from today that were added
new_articles_count = (df['Date'] == str(datetime.date.today())).sum()
print(f'{new_articles_count} articles from today were added')

df.to_csv(filepath, index=False)
print(f"resaved sans duplicates")O