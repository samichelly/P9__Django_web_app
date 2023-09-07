# DJANGO - LITReview

---

Ce projet est une application Web construite avec Django qui permet aux utilisateurs de créer des tickets et des critiques (reviews). Les utilisateurs peuvent également suivre d'autres utilisateurs et voir leurs activités sur leur flux.

## Table des matières

- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)

## Installation

Pour exécuter ce projet localement, suivez ces étapes d'installation :

1. Clonez ce dépôt sur votre machine locale en utilisant la commande suivante :

   ```bash
   git clone https://github.com/samichelly/P9__Django_web_app.git
   ```

2. Accédez au répertoire du projet :

   ```bash
   cd LITReview
   ```

3. Créez un environnement virtuel pour isoler les dépendances :

   ```bash
   python -m venv venv
   ```

4. Activez l'environnement virtuel (selon votre système d'exploitation) :

   - Sur Windows :

     ```bash
     venv\Scripts\activate
     ```

   - Sur macOS et Linux :

     ```bash
     source venv/bin/activate
     ```

5. Installez les dépendances à partir du fichier `requirements.txt` :

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Créez un fichier `.env` à la racine du projet et configurez les variables d'environnement suivantes :

   ```
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   DJANGO_DB_NAME=your_database_name
   DJANGO_DB_USER=your_database_user
   DJANGO_DB_PASSWORD=your_database_password
   DJANGO_DB_HOST=your_database_host
   DJANGO_DB_PORT=your_database_port
   ```

   Assurez-vous de remplacer `your_secret_key_here`, `your_database_name`, `your_database_user`, `your_database_password`, `your_database_host`, et `your_database_port` par les valeurs appropriées.

2. Appliquez les migrations pour créer la base de données :

   ```bash
   python manage.py migrate
   ```

## Utilisation

1. Démarrez le serveur de développement Django :

   ```bash
   python manage.py runserver
   ```

2. Accédez à l'application dans votre navigateur à l'adresse `http://localhost:8000`.

3. Vous pouvez maintenant vous inscrire, vous connecter, créer des tickets, des critiques, suivre d'autres utilisateurs et interagir avec l'application.
