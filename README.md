# Agent-AI - Génération automatique de tests

Ce projet analyse la structure d'un dépôt Git (GitHub, GitLab, Bitbucket) et génère un plan de tests et des tests unitaires via un backend FastAPI. Une petite interface web permet d'entrer l'URL du dépôt et de voir la réponse du serveur en streaming.

## Prérequis
- Python 3.10+ (ou 3.8+)
- Un compte OpenAI et la variable d'environnement `OPENAI_API_KEY` définie dans `.env`

## Configuration des variables d'environnement
Créez un fichier `.env` à la racine du projet en copiant le fichier `.env.example`, puis renseignez les variables nécessaires (par ex. `OPENAI_API_KEY`).

Pour PowerShell (Windows) :

```powershell
copy .env.example .env
```

Pour macOS / Linux :

```bash
cp .env.example .env
```

## Installation (backend)
1. Ouvrir un terminal dans le dossier `agent-ai`.
2. Créer et activer un environnement virtuel :

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1  
```

3. Installer les dépendances :

```powershell
pip install -r requirements.txt
```

## Lancer le backend

```powershell
# depuis le dossier agent-ai

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le service sera disponible sur `http://localhost:8000/`.

Le backend expose notamment :
- `GET  //generate-tests?url_repo=...` -StreamingResponse avec media_type="text/plain"

## Exemples `curl`

- Sous Windows (PowerShell) :

```powershell
curl.exe "http://127.0.0.1:8000/generate-tests?url_repo=https://github.com/shaimaamaidi/simulateur_trafic"
```

## Frontend
- La page web se trouve dans `static/index.html` et s'ouvre automatiquement à la racine `/`.
- L'interface envoie l'URL Git à l'endpoint backend `/generate-tests?url_repo=...` et affiche la réponse en streaming en temps réel.

## Endpoints utiles
- `GET /health` — vérifie que l'API répond
- `GET /generate-tests?url_repo=<URL_GIT>` — lance le traitement du dépôt; la réponse est renvoyée en streaming (`text/plain`).

## Utilisation rapide
1. Démarrer le serveur comme indiqué ci-dessus.
2. Ouvrir `http://localhost:8000/` dans le navigateur.
3. Coller un URL Git valide (ex. `https://github.com/user/repo.git`) et appuyer sur Envoyer.

## Notes
- Le frontend gère la validation basique de l'URL et affiche un message si l'URL n'est pas reconnue comme dépôt Git.
- Les réponses du backend sont lues au fur et à mesure et affichées en temps réel (streaming). Le frontend affiche aussi proprement les blocs de code fournis par le backend en enlevant l'entête de langue (par ex. `python`) et les délimiteurs ```.

## Fichiers principaux
- `main.py` — serveur FastAPI
- `static/index.html` — interface web
- `static/js/chat.js` — logique d'envoi et rendu en streaming
- `static/css/styles.css` — styles de l'interface

