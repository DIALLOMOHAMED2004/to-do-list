# To-Do List

Application web de gestion de tâches personnelles développée avec **Django**. Chaque utilisateur dispose de son propre espace pour organiser ses tâches, suivre leurs échéances et exporter ses données.

## Fonctionnalités

- Inscription avec activation du compte par e-mail, connexion et déconnexion.
- Réinitialisation du mot de passe par e-mail.
- Création, modification, suppression et marquage des tâches comme terminées.
- Description, date d’échéance, priorité (`Low`, `Medium`, `High`) et catégorie (`Work`, `Personal`, `Other`) pour chaque tâche.
- Filtrage par priorité et par date d’échéance exacte.
- Alertes dans la liste pour les tâches non terminées dont l’échéance est dans les deux prochains jours ou déjà dépassée.
- Import et export des tâches au format CSV.
- Interface d’administration Django pour gérer les utilisateurs et les tâches.

Les opérations sur les tâches sont limitées à celles de l’utilisateur connecté. Les alertes d’échéance s’affichent lors de la consultation de la liste ; aucun envoi automatique de rappels par e-mail n’est configuré.

## Technologies

| Composant | Technologie |
| --- | --- |
| Serveur | Python et Django 5.1.3 |
| Base de données | SQLite |
| Interface | Templates Django, HTML, CSS et Bootstrap |
| Authentification | Système d’authentification Django et activation par jeton |

Les dépendances et leurs versions sont définies dans [`requirements.txt`](requirements.txt).

## Installation locale

Prévoir Python 3.12, `pip`, le module `venv` et Git.

### 1. Récupérer le projet

```bash
git clone https://github.com/DIALLOMOHAMED2004/to-do-list.git
cd to-do-list
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows (PowerShell), utiliser :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Installer ensuite les dépendances :

```bash
python -m pip install -r requirements.txt
```

### 3. Configurer les e-mails

L’inscription crée un compte inactif : il faut ouvrir le lien reçu par e-mail pour pouvoir se connecter.

Pour un essai local, ajouter cette ligne à la fin de [`config/settings.py`](config/settings.py) :

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

Les messages et le lien d’activation apparaîtront dans le terminal du serveur. Ouvrir ce lien dans le navigateur pour activer le compte.

Pour envoyer de vrais e-mails, retirer cette ligne et adapter les paramètres de [`config/info.py`](config/info.py) au serveur SMTP utilisé :

```python
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.example.com"
EMAIL_HOST_USER = "votre-adresse@example.com"
EMAIL_HOST_PASSWORD = "votre-mot-de-passe-smtp"
EMAIL_PORT = 587
```

Ces valeurs sont des exemples. Ne pas publier d’identifiants réels dans le dépôt. La configuration actuelle importe directement `config/info.py` et ne charge pas de fichier `.env`.

### 4. Initialiser la base de données et démarrer

Depuis la racine du projet, avec l’environnement virtuel activé :

```bash
python manage.py migrate
python manage.py runserver
```

La commande `migrate` crée la base locale `db.sqlite3`. L’application est ensuite accessible sur [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Pour accéder à l’administration, créer un superutilisateur :

```bash
python manage.py createsuperuser
```

## Utilisation

1. Ouvrir l’accueil et cliquer sur **Sign Up**.
2. Choisir un nom d’utilisateur alphanumérique de 5 à 10 caractères et remplir le formulaire.
3. Activer le compte via le lien d’activation envoyé par e-mail ou affiché dans le terminal.
4. Se connecter avec **Sign In**, puis ouvrir **MES TACHES**.
5. Créer des tâches, appliquer les filtres et utiliser les actions **Modifier**, **Supprimer** ou **Compléter**.

| Page | Chemin |
| --- | --- |
| Accueil | `/` |
| Inscription | `/signup` |
| Connexion | `/signin` |
| Réinitialisation du mot de passe | `/password_reset/` |
| Liste des tâches | `/task/list/` |
| Création d’une tâche | `/task/create/` |
| Export CSV | `/task/export/` |
| Administration | `/admin/` |

Se connecter avant d’ouvrir les pages de tâches : la redirection automatique des visiteurs utilise actuellement l’URL Django par défaut `/accounts/login/`, qui n’est pas définie dans ce projet.

## Format CSV

Depuis la liste des tâches, **Exporter les tâches** télécharge un fichier `tasks.csv` contenant toutes les tâches du compte, indépendamment des filtres affichés. **Importer les tâches** permet de sélectionner un fichier `.csv` encodé en UTF-8.

Respecter cet ordre de colonnes, avec une ligne d’en-tête et une virgule comme séparateur :

```csv
Title,Description,Due Date,Priority,Category,Completed
Préparer le rapport,Rassembler les résultats,2026-10-01,High,Work,False
Faire les courses,Acheter du pain,2026-10-02,Low,Personal,True
```

- Dates au format `AAAA-MM-JJ`.
- Priorités : `Low`, `Medium` ou `High`.
- Catégories : `Work`, `Personal` ou `Other`.
- État terminé : `True` ou `False`.

L’import ajoute de nouvelles tâches à chaque exécution, y compris si elles existent déjà. La validation du fichier est limitée : respecter les six colonnes et les formats indiqués.

## Structure du projet

```text
to-do-list/
├── authentification/   # Inscription, connexion et activation des comptes
├── config/             # Paramètres Django, configuration e-mail et routes principales
├── task/               # Modèles, formulaires, vues et migrations des tâches
├── templates/          # Pages HTML de l’application
├── static/             # Styles CSS et fichiers Bootstrap
├── manage.py           # Commandes de gestion Django
├── requirements.txt    # Dépendances Python
└── README.md
```

## Vérifications

```bash
python manage.py check
python manage.py test
```

La première commande vérifie la configuration Django. Les fichiers de tests des applications sont actuellement des squelettes sans cas de test.

La configuration fournie est destinée au développement local (`DEBUG = True`). Un déploiement nécessite notamment une clé secrète externe au dépôt, `DEBUG = False`, des hôtes autorisés et une configuration adaptée pour les fichiers statiques et les e-mails.
