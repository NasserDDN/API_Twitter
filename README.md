DANDANA Nasser

# Projet SaaS Twitter

L'objectif de ce projet est de recréer Twitter (de manière très simplifiée).

### Statuts des CIs

CI Pull Request : 
![Generic badge](https://github.com/HakimCodage/4A_ILC_Dandana/actions/workflows/Pull_Request.yml/badge.svg)

## Composition du projet

Le projet est composé: 
* d'un backend: une API Python/Flask 
* d'un frontend utilisant VueJS

## L'API

L'API sera responable de traiter les requêtes envoyées par l'utilisateur, qui lui, enverra ses requêtes depuis l'interface utilisateur (càd le frontend). Pour stocker les données, cette API utilisera une base redis qui est une base de données clé valeur facilement utilisable.

## Le frontend

Le frontend sera l'interface graphique de l'utilisateur. Cette interface sera constituée de plusieurs pages web permettant de couvrir toutes les fonctionnalités de l'API.

## Les fonctionnalités

Ce couple API/Frontend répond aux fonctionnalités suivantes :

* Tweeter et enregistrer les tweets dans redis
* Retweeter
* Afficher tous les tweets
* Afficher les sujets
* Afficher les tweets liés à une personne
* Afficher les tweets liés à un sujet
* Créer un compte utilisateur
* Se connecter avec un compte utilisateur

La façon dont l'API et le frontend gère et exploite ces fonctionnalités sera détaillée dans les README qui leur sont consacrés.

## Procédure pour utiliser ce SaaS

### Avec des conteneurs

Commencez par démarrer votre logiciel Docker Desktop.

Il y a 2 Dockerfile dans ce projet : 1 pour le backend et 1 pour le frontend.

J'ai utilisé un `docker-compose` pour exécuter ces Dockerfiles ensemble. Pour build celui-ci, exécutez la commande suivante dans un terminal en vous plaçant à la racine du projet:

```
docker-compose up -d --build
```

Parfois, lors de l'exécution du docker-compose, il y a une erreur : "All browser targets in the browserslist configuration have supported ES module. Therefore we don't build two separate bundles for differential loading.".

J'ai essayé de la comprendre mais sans succès. Je pense l'avoir résolu en modifiant la version de node dans le Dockerfile du frontend.

Ensuite, vous pouvez run le docker-compose avec la commande :

`docker-compose up`

Ce `docker-compose` exécute les Dockerfiles du backend et du frontend et crée un conteneur Redis.

Vous pourrez accéder à la page du frontend à l'adresse [localhost:8000](http://127.0.0.1:8000/)

### Sans conteneurs (pas conseillé car procédure plus longue et moins pratique)

(J'ai conservé cette partie dans le README mais elle est devenue inutile puisque j'ai réussi la conteneurisation)

D'abord, il faut modifier légèrement le fichier API.py : au début du fichier lorsque les bases redis sont créés, il faut pour chaque déclaration, modifier le paramètre `host` et lui attribuer la valeur `'localhost'` à la place de `'service_redis'`. (Il faudra évidemment faire la modification dans l'autre sens si vous voulez utiliser les conteneurs par la suite)

Il faut aussi lancer un conteneur Redis à l'aide de la commande suivante :

```
docker run -d -p 6379:6379 --name myredis --network redisnet redis
```

#### Installer les dépendances

Les dépendances liées au backend sont listées dans le fichier `requirements.txt` dans le dossier backend. Pour installer toutes ces dépendances, entrez la commande suivante dans un terminal en vous plaçant dans le dossier `backend` :

```
pip install -r requirements.txt
```

Ensuite, il faudra exécuter cette suite de commandes :

```
set (ou export suivant le type de terminal) FLASK_APP=chemin/du/fichier/API.py
```

```
flask run
```

Pour pouvoir accéder aux pages web du frontend, exécutez les commandes suivantes dans un terminal Powershell en vous plaçant dans le dossier `frontend` :

```
npm install
```

```
npm run build
```

Cette fois-ci, la page web sera disponible à l'adresse [localhost:8080](http://localhost:8080/).

### Données par défaut

Des données sont générées par défaut dans la base `Redis`. Si vous voulez éviter cette génération, vous pouvez supprimer la ligne 36 du fichier `API.py`: `load_content()`.

Si vous ne voulez pas que les données se suppriment à chaque redémarrage des conteneurs, il faut supprimer la ligne 33 du fichier `API.py` : `tweets_db.flushall()`.

Les 2 utilisateurs créés par défaut possèdent un mot de passe identique à leur pseudo. 









