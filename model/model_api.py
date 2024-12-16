import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

def load_data():
    return pd.read_csv('data/articles.csv')

def load_model():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def load_embeddings():
    return np.load('data/embeddings.npy')

def get_most_similar(sentence:str,
                     embeddings: List[List[float]],
                     model: SentenceTransformer,
                     articles: pd.DataFrame,
                     n:int=5) -> List[Dict[str, Any]]:

    query_embedding = model.encode(sentence).reshape(1, -1)
    
    similarities = cosine_similarity(np.array(embeddings), query_embedding).flatten()
    
    top_n_indices = similarities.argsort()[-n:][::-1]
    
    most_similar = []
    for idx in top_n_indices:
        article = articles.iloc[idx]
        date = datetime.strptime(article['date'], '%Y-%m-%dT%H:%M:%S%z')
        formatted_date = date.strftime('%d/%m/%y')
        most_similar.append({
            'title': article['title'],
            'url': article['url'], 
            'date': formatted_date,
            'description': article['summary']
        })
    
    return most_similar