# AfricAI

## Description
AfricAI est un projet visant à collecter, traiter et exploiter des données juridiques provenant de divers sites web de plusieurs pays africains. En utilisant Kedro pour orchestrer les pipelines de traitement des données, AfricAI construit une base de connaissances interrogeable via un système de RAG (Retrieval-Augmented Generation) optimisé par ChromaDB et des modèles d'embeddings.

## Objectifs
- Scraper des données juridiques sous divers formats (PDF, images scannées, texte brut, etc.).
- Extraire et traiter les informations à l'aide d'une pipeline Kedro.
- Charger et analyser les documents (lecture de texte, extraction de tableaux et images, parsing des données).
- Prétraiter les données (segmentation, nettoyage du texte, suppression des redondances, normalisation).
- Construire une base de données ChromaDB et générer des embeddings pertinents.
- Mettre en place une architecture RAG pour interroger les données.
- Développer des agents intelligents capables de répondre aux questions des utilisateurs à partir des données traitées.

## Architecture
AfricAI repose sur une architecture modulaire et scalable :
1. **Collecte de données** : Scraping de sites juridiques africains et téléchargement de documents.
2. **Extraction & Traitement** : Utilisation de PyPDFLoader et d'outils OCR pour extraire le texte et les tables.
3. **Prétraitement** : Nettoyage et normalisation des données.
4. **Stockage** : Indexation des données dans ChromaDB avec des embeddings pour une recherche rapide.
5. **Recherche & RAG** : Implémentation d'une recherche intelligente augmentée par le contexte des documents.
6. **Agents conversationnels** : Développement de bots capables de répondre aux requêtes des utilisateurs en interrogeant la base de connaissances.

## Installation
```bash
# Cloner le projet
git clone https://github.com/akacarlll/LawIntelAfrica.git
cd LawIntelAfrica

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation
1. Lancer le scraping : `python scripts/scrape.py`
2. Exécuter la pipeline Kedro : `kedro run`
3. Interroger la base de données avec l'agent : `python scripts/query_agent.py`

## Technologies utilisées
- **Kedro** : Orchestration des pipelines de traitement.
- **ChromaDB** : Stockage et indexation des embeddings.
- **OCR & NLP** : Extraction et traitement des documents.
- **LangChain** : Construction des agents conversationnels.
- **FastAPI** : Interface pour exposer l'API de recherche et de requêtage.

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à proposer une pull request.

## Licence
MIT License

