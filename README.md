DANDANA Nasser

# Projet SaaS Twitter

L'objectif de ce projet est de recréer Twitter (de manière très simplifiée).

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

La façon dont l'API et le frontend gère et exploite ces fonctionnalités sera détaillée dans le README qui leur est consacré.

## Procédure pour utiliser ce SaaS

### Avec des conteneurs

Je n'ai pas réussi à mettre le frontend dans un conteneurs. Cependant, le backend peut être mis dans un conteneur grâce au `docker-compose` à la racine du projet. Vous pouvez build ce fichier à l'aide de la commande : 

`docker-compose up -d --build`

et run le docker-compose avec la commande :

`docker-compose up`

Ce `docker-compose` exécute le Dockerfile du backend et run un conteneur Redis.

Le Dockerfile du frontend est aussi présent dans le dossier `frontend` mais n'est pas fonctionnel. Vous pouvez essayer d'exécuter le Dockerfile du frontend de votre côté. Il vous faut installer nginx et ensuite suivre ce [tutoriel](https://medium.com/bb-tutorials-and-thoughts/how-to-serve-vue-js-application-with-nginx-and-docker-d8a872a02ea8) (c'est celui que j'ai suivi).

Il vous faudra donc cloner ce dépôt sur votre machine pour pouvoir l'utiliser en local.

### Sans conteneurs

#### Installer les dépendances

Il faut d'abord build et lancer un conteneur Redis à l'aide de la commande suivante :

```
docker run -d -p 6379:6379 --name myredis --network redisnet redis
```

Vous pourrez utiliser 
```
docker restart myredis
```
si vous décidez de redémarrer le conteneur dans le futur.

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

Pour pouvoir accéder aux pages web du frontend, il faut d'abord installer [Node](https://nodejs.org/en).

Ensuite, exécutez la commande suivante dans un terminal en vous plaçant dans le dossier `frontend` :

```
npm run serve
```

La page web sera donc disponible à l'adresse [localhost:8080](http://localhost:8080/).

### Statuts des CIs

CI Pull Request : 
![Generic badge](https://github.com/HakimCodage/4A_ILC_Dandana/actions/workflows/Pull_Request.yml/badge.svg)







