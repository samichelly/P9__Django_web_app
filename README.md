# DJANGO - LITReview

---

Ce projet est une application Web construite avec Django qui permet aux utilisateurs de créer des tickets et des critiques (reviews). Les utilisateurs peuvent également suivre d'autres utilisateurs et voir leurs activités sur leur flux.

## Table des matières

- [Installation](#installation)
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

## Utilisation

1. Démarrez le serveur de développement Django :

   ```bash
   python manage.py runserver
   ```

2. Accédez à l'application depuis le navigateur de votre choix, se rendre à l'adresse → http://127.0.0.1:8000/ .

3. Vous pouvez maintenant vous inscrire, vous connecter, créer des tickets, des reviews, suivre d'autres utilisateurs et intéragir ensemble.

### Django administration
Identifiant : Admin | Mot de passe : litreview

→ http://127.0.0.1:8000/admin/
