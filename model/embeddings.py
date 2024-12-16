import feedparser
import pandas as pd
import json
import numpy as np

from datetime import datetime
from sentence_transformers import SentenceTransformer

def load_data():
    '''
    Load the data from the gossip_scrapper output file
    '''
    output_path_vsd = "gossip_scrapper/vsd_articles.jl"

    data = []
    with open(output_path_vsd, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON : {e}")

    return pd.DataFrame(data)

def convert_date(date_str: str) -> str:
    date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    return date_obj.strftime('%Y-%m-%dT%H:%M:%S%z')[:-4] + '00:00'

def add_rss(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Add the RSS feeds to the dataframe
    '''
    rss_feeds = [
        "https://www.vsd.fr/rss",
        "https://www.public.fr/rss"
    ]

    articles = []

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary
            })

    df_rss = pd.DataFrame(articles)
    df_rss = df_rss.rename(columns={
        'link': 'url',
        'published': 'date'
    })

    df_rss['date'] = df_rss['date'].apply(convert_date)
    return pd.concat([df, df_rss], ignore_index=True)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Clean the data
    '''
    df = df.drop_duplicates(subset=['title'])
    df = df.dropna(subset=['title', 'summary'])
    return df

def save_data(df: pd.DataFrame):
    '''
    Save the data to a CSV file
    '''
    df.to_csv('data/articles.csv', index=False)

def encode_articles(df: pd.DataFrame, model):
    '''
    Encode the articles with the SentenceTransformer model
    '''
    embeddings = model.encode(df['title'].values)
    np.save('data/embeddings.npy', embeddings)

def main():
    '''
    Main function
    '''
    print('Loading data...')
    df = load_data()
    df = add_rss(df)
    df = clean_data(df)
    print('Data loaded and cleaned')
    save_data(df)
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print('Encoding articles...')
    encode_articles(df, model)
    print('Articles encoded')

if __name__ == '__main__':
    main()

