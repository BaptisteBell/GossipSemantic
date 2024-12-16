# Gossip Semantic Search

## Installation des prérequis

Assurez-vous d'avoir **Python 3.10** minimum installé.

Installez les dépendances nécessaires avec :

```bash
pip install -r requirements.txt
```

## Lancer l'API

Pour démarrer l'API avec **Uvicorn**, exécutez :

```bash
uvicorn api:app --reload
```

L'API sera accessible à l'adresse : `http://127.0.0.1:8000`

## Scraper les données

Le dossier `gossip_scrapper` contient le code pour scraper les articles avec **Scrapy**.

### Scraper les articles de VSD et Public :

```bash
cd gossip_scrapper
scrapy crawl vsd -o vsd_articles.csv
scrapy crawl public -o public_articles.csv
```

### Création des embeddings
```bash
python .\model\embeddings.py 
```

## Structure des dossiers

```
.
├── gossip_scrapper/      # Contient le code Scrapy pour scraper les données
│   ├── spiders/
│   └── ...
│
├── data/                 # Contient les données utiles au modèle et à l'API
│   ├── articles.csv       # Articles au format CSV
│   └── embeddings.npy       # Embeddings utilisés pour la recherche sémantique
│
├── model/                # Contient les fichiers liés au modèle
│   ├── model_api.py                # script des fonsction du model
│   ├── embeddings.py                # script des fonctions de traitements des données et création des embeddings des articles
│   └── GossipSemanticSearch.ipynb # Notebook pour le test des données
│
├── templates/            # Contient le front-end de l'application
│   └── index.html             # Code HTML pour l'interface utilisateur
│
└── api.py                # Code de l'API FastAPI
```

## Utilisation du Notebook

Le notebook `GossipSemanticSearch.ipynb` permet de :

1. Charger les données.
2. Nettoyer et transformer les données.
3. Générer et tester les embeddings pour la recherche sémantique.