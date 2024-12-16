# Gossip Semantic Search

## Installing prerequisites

Make sure you have at least **Python 3.10** installed.

Install the necessary dependencies with 

```bash
pip install -r requirements.txt
```

## Launch API

To start the API with **Uvicorn**, run :

```bash
uvicorn api:app
```

The API can be accessed at: `http://127.0.0.1:8000`

## Data scraping

The `gossip_scrapper` folder contains the code for scrapping articles with **Scrapy**.

The scraping has already been completed, and the data is available in the `.jl` files for direct use with the API.

> Note: Scraping data can be very time-consuming, depending on the number of articles you wish to retrieve.


### Scrape articles from VSD and Public :

```bash
cd gossip_scrapper
scrapy crawl vsd -o vsd_articles.jl
scrapy crawl public -o public_articles.jl
```

## Creating embeddings

The `embeddings.py` script is used to clean data and generate embeddings for articles.

```bash
cd ..
python model/embeddings.py
```

## Folder structure

```
.
├── gossip_scrapper/              # Contains Scrapy code to scrape data
│   ├── spiders/
│   └── ...
│
├── data/                         # Contains data useful to the model and API
│   ├── articles.csv          # Articles informations in CSV format
│   └── embeddings.npy            # Embeddings used for semantic search
│
├── model/                        # Contains files related to the model
│   ├── model_api.py              # Functions called by the APII
│   ├── embeddings.py             # Script for data cleansing and embedding creation
│   └── GossipSemanticSearch.ipynb # Notebook for testing code and visualizing data transformations (not useful)
│
├── templates/                    #  Contains the application's front-end
│   └── index.html                # HTML code for user interface
│
└── api.py                        # FastAPI API code
```

## Using the Notebook

The `GossipSemanticSearch.ipynb` notebook allows you to :

1. Load data.
2. View and test code.
3. Observe the various stages of data transformation.

> **Note:** The notebook is for testing and exploring code only. It does not generate embeddings for the API.