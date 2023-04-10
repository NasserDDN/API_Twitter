import redis
import bcrypt
import datetime
import json


#Base pour stocker les tweets
tweets_db = redis.Redis(host='service_redis', port=6379, charset="utf-8", decode_responses=True, db=0)

#Base contenant les tweets de chaque utilisateur (retweets inclus)
users_db = redis.Redis(host='service_redis', port=6379, charset="utf-8", decode_responses=True, db=1)

#Base contenant la liste des sujets
hashtag_db = redis.Redis(host='service_redis', port=6379, charset="utf-8", decode_responses=True, db=2)

#Base contenant la liste des comptes et leur mot de passe encrypté
account_db = redis.Redis(host='service_redis', port=6379, charset="utf-8", decode_responses=True, db=3)

#Base pour stocker l'utilisateur actuel
actual_user_db = redis.Redis(host='service_redis', port=6379, charset="utf-8", decode_responses=True, db=4)


def load_content():
    
    user1_username = "Nasser"
    user1_password = "Nasser"

    user2_username = "Quentin"
    user2_password = "Quentin"

    #############################
    #Inscription des utilisateurs
    #############################

    #Utilisateur 1
    encrypt_pwd = bcrypt.hashpw(user1_password.encode('utf-8'), bcrypt.gensalt())
    account_db.set(user1_username, encrypt_pwd)

    #Utilisateur 2
    encrypt_pwd = bcrypt.hashpw(user2_password.encode('utf-8'), bcrypt.gensalt())
    account_db.set(user2_username, encrypt_pwd)

    ########################
    #Connexion Utilisateur 1
    ########################

    #J'ai simplifié la connexion (vérification de compte, mot de passe)
    actual_user_db.set("actual", str(user1_username))

    #####################
    #Tweets Utilisateur 1
    #####################

    dict = {}
    dict["author"] = user1_username
    dict["tweet"] = "Je suis le premier utilisateur #Premier #Heureux"

    #J'ai simplifié l'ajout des hashtags
    hashtag = []
    hashtag.append("#Premier")
    hashtag.append("Heureux")
    hashtag = json.dumps(hashtag)
    dict["hashtags"] = hashtag

    #Récupération du timestamp décalé de -5000 (+ d'une heure en arrière)
    timestamp1 = datetime.datetime.now().timestamp()
    timestamp1 -= 5000

    #Enregistre le tweet au timestamp actuel
    tweets_db.hmset(timestamp1, dict)

    #Attribut le tweet à l'utilisateur
    users_db.rpush(user1_username, timestamp1)

    #Ajout des hashtags à la base qui regroupe les sujets
    #Simplifié
    hashtag_db[len(hashtag_db.keys())] = "#Premier"
    hashtag_db[len(hashtag_db.keys())] = "#Heureux"

    ########################
    #Connexion Utilisateur 2
    ########################

    #J'ai simplifié la connexion (vérification de compte, mot de passe)
    actual_user_db.set("actual", str(user2_username))

    #####################
    #Tweets Utilisateur 2
    #####################

    dict = {}
    dict["author"] = user2_username
    dict["tweet"] = "Je suis le second utilisateur #Deuxième #Heureux"

    #J'ai simplifié l'ajout des hashtags
    hashtag = []
    hashtag.append("#Deuxième")
    hashtag.append("Heureux")
    hashtag = json.dumps(hashtag)
    dict["hashtags"] = hashtag

    #Récupération du timestamp
    timestamp2 = datetime.datetime.now().timestamp()

    #Enregistre le tweet au timestamp actuel
    tweets_db.hmset(timestamp2, dict)

    #Attribut le tweet à l'utilisateur
    users_db.rpush(user2_username, timestamp2)

    #Ajout des hashtags à la base qui regroupe les sujets
    #Simplifié
    hashtag_db[len(hashtag_db.keys())] = "#Deuxième"

    ########
    #Retweet
    ########

    #Utilisateur 2 retweet le tweet de l'Utilisateur 1
    #Simplifié aussi
    users_db.rpush(user2_username, timestamp1)

    #Utilisateur 2 son propre tweet
    #Simplifié aussi
    users_db.rpush(user2_username, timestamp2)






