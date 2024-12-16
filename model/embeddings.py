import feedparser
import pandas as pd
import json
import numpy as np

from datetime import datetime
from sentence_transformers import SentenceTransformer

def load_data(output_path: str) -> pd.DataFrame:
    '''
    Load the data from the gossip_scrapper output file
    '''
    data = []
    with open(output_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON : {e}")

    return pd.DataFrame(data)

def load_all_data():
    output_path_vsd = "gossip_scrapper/vsd_articles.jl"
    output_path_public = "gossip_scrapper/public_articles.jl"

    df_vsd = load_data(output_path_vsd)
    df_public = load_data(output_path_public)

    return pd.concat([df_vsd, df_public], ignore_index=True)

def convert_date(date_str: str) -> str:
    date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    return date_obj.strftime('%Y-%m-%dT%H:%M:%S%z')[:-4] + '00:00'

def concat_data(df: pd.DataFrame, df_rss: pd.DataFrame) -> pd.DataFrame:
    df_concat = pd.concat([df, df_rss], ignore_index=True)
    return df_concat

def add_rss() -> pd.DataFrame:
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

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Clean the data
    '''
    df_cleaned = df.replace("N/A", pd.NA).dropna()
    df_cleaned = df_cleaned.drop_duplicates(subset=['url'])
    return df_cleaned

def save_data(df: pd.DataFrame):
    '''
    Save the data to a CSV file
    '''
    df.to_csv('data/articles.csv', index=False)

def encode_articles(df: pd.DataFrame, model):
    '''
    Encode the articles with the SentenceTransformer model
    '''
    sentences = df['title'].tolist()
    embeddings = model.encode(sentences)
    np.save('data/embeddings.npy', embeddings)

def main():
    '''
    Main function
    '''
    print('Loading data...')
    df = load_all_data()
    df_rss = add_rss()
    df = concat_data(df, df_rss)
    
    df = clean_data(df)
    
    print('Data loaded and cleaned')
    save_data(df)
    
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    print('Encoding articles...')
    encode_articles(df, model)
    
    print('Articles encoded')

if __name__ == '__main__':
    main()

