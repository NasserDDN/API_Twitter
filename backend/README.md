# Backend

Pour le backend, j'ai utilisé Python et Flask. 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)


## Structure de données de Redis

1. La base pour stocker les tweets (`tweets_db`). Un tweet est stocké de la manière suivante :
   ```
   key=timestamp, value='{"author”: username, "tweet”: message, "hashtag": [hashtag1, hashtag2...]}'
   ```
   
2. La base contenant les clés des tweets de chaque utilisateur, retweets inclus (`users_db`) :
   ```
   key=username, value=[timestamp_1, timestamp_2, timestamp_3...]
   ```
   
3. La base contenant la liste des sujets existants (`hashtag_db`) :
   ```
   key=id (compteur qui s'incrémente), value=hashtag
   ```
   
4. La base contenant les comptes et les mots de passe encryptés des utilisateurs (`account_db`) :
   ```
   key=username, value=encrypted_password
   ```
   
5. Base pour stocker l'utilisateur actuellement connecté ou connecté en tant qu'invité (`actual_user_db`) :
   ```
   key="actual", value=username
   ```
   
   
   
## Les routes
&nbsp;

L'API est composée de 5 routes différentes.

**POST** `/postTweet`

Enregistre un tweet dans la base Redis.

Paramètre nécessaire : 
```
'{"author": username, "tweet": message}'
```

Le tweet est ajouté à la base `tweets_db` et il est ajouté à la liste des tweets de l'auteur dans la base `users_db`.

La fonction associée à cette route va détecter si il y a des hashtags dans le tweet et les ajouter à la base `hashtag_db` si les sujets ne sont pas déjà présents dans la base.

Return : Le dictionnaire passé en paramètre de la requête.

&nbsp;
   
   
**GET** `/`

Retourne les tweets et les sujets enregistrés dans la base Redis.

Paramètre nécessaire : `aucun`

Les tweets sont triés du plus au moins récent. La fonction associée à cette route s'occupe de traiter le timestamp du tweet pour avoir une date au bon format dans le frontend.

Return : 
```
'{key = "tweets", value = [{"author": username, "tweet": message, "id": timestamp, "time": date}], key = "sujets", value = [hashtag1, hashtag2 ...]}'
```
Pour que cela soit plus clair, nous avons :
* Une liste de tous les tweets => `[{tweet1}, {tweet2} , ...]`
* Une liste des sujets => `[sujet1, sujet2, ...]`

Et ces 2 listes sont insérées dans un dictionnaire qui est retourné à la fin de la fonction.

&nbsp;


**PUT** `/`

Retourne tous les tweets liés à un utilisateur ou à un sujet.

Paramètre nécessaire :

* Si nous voulons les tweets liés à un utilisateur:
  ```
  '{"data": u-username}'
  ```

* Ou si nous voulons les tweets liés à un sujet :
  ```
  '{"data": h-sujet}'
  ```
  
  Return : 
  ```
  '[{tweet1}, {tweet2}]'
  ```
  
  OU 
  ```
  '"ERROR"'
  ```
  Si le paramètre de la requête n'est pas bon.
  
  
  

**PUT** `/inscription`

Enregistre un compte dans la base, accepte/refuse une connexion ou enregistre un retweet suivant le paramètre qui est fourni avec la requête.

Si requête de retweet :
  
  * Paramètre nécessaire :
    ```
    '{"user": utilisateur_qui_veut_retweeter, "author": auteur_du_tweet, "id": timestamp_du_tweet, "requestType": "retweet" }'
    ```
    
    La fonction prend en compte l'annulation d'un retweet (si l'utilisateur retweet un tweet qu'il a déjà retweeté auparavant).
    
    Un utilisateur peut aussi retweet ses propres tweets.
    
    Return : 
    * `"0"` si c'est un retweet
    * `"1"` si c'est une annulation de retweet
     
    
    
Si requête de connexion :
  
  * Paramètre nécessaire :
    ```
    '{"username": username, "password": password, "requestType": "signin" }'
    ```
    
    OU
    
    ```
    '{"username": "invité", "password": "invité", "requestType": "signin" }'
    ```
    
    Si l'utilisateur ne veut pas se connecter mais continuer en tant qu'invité.
    
    Return : 
    * `"Impeccable"` si la connexion s'est bien déroulé
    * `"ERROR CODE 1"` si le mot de passe est incorrect
    * `"ERROR CODE 2"` si le le pseudo n'existe pas


Si requête d'inscription :
  
  * Paramètre nécessaire :
    ```
    '{"username": username, "password": password, "requestType": "signup" }'
    ```
    
    Return : 
    * `"Impeccable"` si l'inscription s'est bien déroulé
    * `"ERROR CODE 1"` si le pseudo existe déjà



**POST** `/`

Retourne le pseudo de l'utilisateur actuel.

Paramètre nécessaire : aucun

Return : `utilisateur_actuel`






   
   

   
   
   
   

  
