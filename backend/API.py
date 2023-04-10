from flask import Flask, jsonify
from flask import request
import sys
import json #Pour sauvegarder des dictionnaires dans les redis
import datetime #Pour les timestamp
import redis
from flask_cors import CORS
import bcrypt #Pour encrypter les mots de passes
from script import *


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


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

#Vider les bases redis
tweets_db.flushall()

#Données par défaut dans la base redis
load_content()


#Enregistrer un tweet
@app.route('/postTweet', methods=['POST']) 
def tweeter(): 
                                                                
    if request.method == 'POST':

        #Récupération des paramètres de la requête
        record = json.loads(request.data)
        author = str(record['author'])
        tweet = str(record['tweet'])

        #Création du dictionnaire
        dict = {}
        dict["author"] = author
        dict["tweet"] = tweet
        
        ##############################
        #Vérifier si il y a un hashtag
        ##############################
        text = tweet.split()

        #Liste qui contiendra 0, 1 ou plusieurs sujets
        hashtag = []

        is_an_hashtag = False

        #Parcours des mots du texte
        if(len(text) > 1) :
            for word in text :

                #Si un hashtag est détecté
                if word[0] == "#":
                    
                    #Ajout du hashtag à la liste
                    hashtag.append(word)

                    is_an_hashtag = True

                

        elif (len(text) == 1):
            for word in text :
                if word[0] == "#":
                    print("Il y a un HASHTAG 2")
                    
                    #Ajout du hashtag à la liste
                    hashtag.append(word)

                    is_an_hashtag = True

        
        
        #Clés pour parcourir la base
        keys = hashtag_db.keys()
        
        #Si le tweet contient un sujet
        if is_an_hashtag:

            exist = False

            #Parcours des sujets du tweet
            for hash in hashtag:

                #Parcours de la base
                for key in keys:

                    value = hashtag_db[key]

                    #On vérifie si le hashtag est déjà dans la base
                    if (hash == value):

                        exist = True
                
                #Si le hashtag n'existe pas dans la base on l'ajoute
                if not exist:

                    hashtag_db[len(hashtag_db.keys())] = hash
                
                exist = False

        #Si pas d'hashtag dans le texte
        else:
            
            hashtag.append("NoHashtags")


        #Ajout de la liste d'hashtags au dictionnaire
        hashtag = json.dumps(hashtag)
        dict["hashtags"] = hashtag
        
        #Récupération du timestamp
        current_time = datetime.datetime.now().timestamp()

        #Enregistre le tweet au timestamp actuel
        tweets_db.hmset(current_time, dict)

        #Attribut le tweet à l'utilisateur
        users_db.rpush(author, current_time)
        
        return jsonify(record)
        
        
       
        
#Récupérer et retourne les tweets et les sujets
@app.route("/", methods=['GET']) 
def afficher_tweets():   
    if request.method == 'GET': 

    
        #Déclaration des listes
        list_tweets = []
        list_sujets = []

        #Récupération des keys dans la base de tweets
        keys = tweets_db.keys()

        #Trier les clés pour afficher les tweets du plus au moins récent
        keys.sort(reverse=True)      #(reverse = True pour ordre décroissant)
            
        #Parcours des tweets
        for key in keys :

            #Récupération du dictionnaire
            value = tweets_db.hgetall(key)

            #Id unique pour chaque tweet
            value["id"] = key

            #Récupération du timestamp
            current_time = datetime.datetime.now().timestamp()

            #Différence pour savoir depuis combien de temps le tweet est publié
            difference  = current_time - float(key)

            #Si le tweet a été publié il y a moins d'une heure
            if(difference < 3600):
                
                #Conversion en minutes
                nb_minutes = int(difference / 60)

                value["time"] = str(nb_minutes) + 'min'

                #Ajout à la liste des tweets
                list_tweets.append(value)


            #Si le tweet a été publié il y a plus de 24h
            elif(difference > 86400):
                
                #Conversion au format Jour - Mois - Année
                date_time = datetime.datetime.fromtimestamp(float(key))
                str_date_time = date_time.strftime("%d %B %Y")

                value["time"] = str_date_time

                #Ajout à la liste des tweets
                list_tweets.append(value)

            #Si le tweet a été publié il y a moins de 24h
            else :

                #Conversion pour avoir le nombre d'heures
                nb_hours = int(difference / 3600)

                value["time"] = str(nb_hours) + 'h'

                #Ajout à la liste des tweets
                list_tweets.append(value)
    
        #Récupération des keys dans la base de hashtag
        keys = hashtag_db.keys()

        #Parcours des keys
        for key in keys :

            #Récupération du dictionnaire
            value = hashtag_db.get(key)

            list_sujets.append(value)

        dict = {}
        dict["tweets"] = list_tweets
        dict["sujets"] = list_sujets

        
        return jsonify(dict)
    
def convertTimestamp(item, difference):
    #Si le tweet a été publié il y a moins d'une heure
                if(difference < 3600):

                    print("Entrée dans la fonction")
            
                    nb_minutes = int(difference / 60)

                    return str(nb_minutes) + 'min'

                #Si le tweet a été publié il y a plus de 24h la date sera affichée
                elif(difference > 86400):
                
                    date_time = datetime.datetime.fromtimestamp(float(item))
                    str_date_time = date_time.strftime("%d %B %Y")

                    return str_date_time

                #Si le tweet a été publié il y a moins de 24h le nombre d'heures est affiché
                else :
                    nb_hours = int(difference / 3600)

                    return str(nb_hours) + 'h'
 

#Afficher tous les tweets liés à une personne ou à un sujet
#appel dans un autre terminal avec : curl -X GET http://127.0.0.1:5000/u-username or h-hashtag (with the #)
@app.route("/", methods=['PUT']) 
def afficher_tweets_personne(object=None):   

    if request.method == 'PUT': 

        #Récupération des paramètres
        record = json.loads(request.data)
        username = str(record['data'])

        #Déclaration de la lkste
        list_tweets = []

        #Si le paramètre est un nom d'utilisateur
        if (username[0] == "u" and username[1] == "-"):

            #Suppression des 2 premiers caractères
            username = username[2:]

            #Parcours de tous les tweets de l'utilisateur
            for item in users_db.lrange(username, 0 , -1):
            
                value = tweets_db.hgetall(item)

                #Récupération du timestamp
                current_time = datetime.datetime.now().timestamp()

                #Différence pour savoir depuis combien de temps le tweet est publié
                difference  = current_time - float(item)

                #Conversion de la différence de temps au bon format
                value["time"] = convertTimestamp(item, difference)

                #Ajout du tweet à la liste
                list_tweets.append(value)

            return jsonify(list_tweets)


        #Si le paramètre est un hashtag
        elif (username[0] == "h" and username[1] == "-"):

            #Suppression des 2 premiers caractères
            sujet = username[2:]

            keys = tweets_db.keys()

            #Parcours des tweets
            for key in keys :

                #Récupération des hashtags si il y en a
                value = tweets_db.hgetall(key)
                hashtags = json.loads(value["hashtags"])

                #Parcours des hashtags
                for hashtag in hashtags:

                    #Si le tweet est lié au hashtag on l'ajoute dans la liste
                    if (sujet == hashtag):

                        #Récupération du timestamp
                        current_time = datetime.datetime.now().timestamp()

                        #Différence pour savoir depuis combien de temps le tweet est publié
                        difference  = current_time - float(key)

                        #Conversion de la différence de temps au bon format
                        value["time"] = convertTimestamp(key, difference)

                        #Ajout du tweet à la liste
                        list_tweets.append(value)

            return jsonify(list_tweets)

        else :
            return jsonify("ERROR")


#Inscription, Connexion, Retweet
@app.route("/inscription", methods=['PUT']) 
def retweet():                                                                

    if request.method == 'PUT': 

        #Récupération des paramètres
        record = json.loads(request.data)

        ########
        #Retweet
        ########
        if(record["requestType"] == "retweet"):
                
            timestamp = float(record["id"])
            user_who_rt = str(record["user"])
            author_of_tweet = str(record["author_of_tweet"])

            #-------------------------------------------#
            #Si l'utilisateur a déjà tweeté ou retweeter#
            #-------------------------------------------#
            if(users_db.exists(user_who_rt) == 1):

                #Compteur
                count = 0
                    
                #Si l'utilisateur veut retweet son propre tweet
                if(user_who_rt == author_of_tweet):
                        
                    #Parcours de tous les tweets de l'utilisateur
                    for item in users_db.lrange(user_who_rt, 0 , -1):

                        #Compte du nombre de fois que son tweet apparait sur son profil
                        if(timestamp == float(item)):
                            count = count +1
                        
                    #Si apparition du tweet plus de 2 fois
                    # => L'auteur du tweet a déjà retweeté son propre tweet
                    # => Il veut donc annuler ce retweet
                    if(count > 1):

                        #Annuler le retweet
                        users_db.lrem(user_who_rt, -1, timestamp)
                        return jsonify("1")
                        
                    #Si il n'a jamais retweeté ce tweet
                    users_db.rpush(user_who_rt, timestamp)
                    return jsonify("0")
                
                #Si l'utilisateur veut retweet le tweet d'un autre
                else:

                    #Parcours de tous les tweets de l'utilisateur
                    for item in users_db.lrange(user_who_rt, 0 , -1):

                        #Si il a déjà retweeté ce tweet
                        if(timestamp == float(item)):

                            #Annulation du retweet
                            users_db.lrem(user_who_rt, -1, timestamp)
                            count = count + 1

                            return jsonify("1")

                    #Si il n'a jamais retweeté ce tweet
                    users_db.rpush(user_who_rt, timestamp)
                    return jsonify("0")

            #------------------------------------------#
            #------------------SINON-------------------#
            #------------------------------------------#
            else:
                #Ajout de la clé du tweet dans la liste des tweets de l'utilisateur qui a retweet
                users_db.rpush(user_who_rt, timestamp)
                return jsonify("0")
            
            
        ########################
        #Si demande de connexion
        ########################
        elif(record["requestType"] == "signin"):

            #Liste des clés de la base
            users = account_db.keys()

            #Récupération du pseudo
            user = str(record["username"])

            #Récupération du mot de passe
            password = str(record["password"])

            #Si l'utilisateur continue en tant qu'invité
            if(user == "invité" and password == "invité"):
                    
                #Actualisation de l'utilisateur en cours
                actual_user_db.set("actual", str(user))

                return jsonify("Impeccable")
                    
            #Parcours des comptes enregistrés
            for key in users:

                #Si le compte existe
                if (str(key) == user):

                    #Si mot de passe correct
                    if bcrypt.checkpw(password.encode('utf-8'), account_db.get(key).encode('utf-8')):

                        #Actualisation de l'utilisateur en cours
                        actual_user_db.set("actual", str(user))

                        return jsonify("Impeccable")
                    
                    #Si mot de passe incorrect
                    else: 
                        return jsonify("ERROR CODE 1")

            #Si le pseudo n'existe pas dans la base
            return jsonify("ERROR CODE 2")

        ############
        #Inscription
        ############    
        elif(record["requestType"] == "signup") :

            #Liste des clés de la base
            users = account_db.keys()
        
            #Récupération du pseudo
            user = str(record["username"])

            #Si le pseudo existe deja
            if user in users:
                 return jsonify("ERROR CODE 1")
            
            #Récupération et encryptage du mot de passe
            password = str(record["password"])

            encrypt_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            #Ajout à la base redis
            account_db.set(user, encrypt_pwd)

            return jsonify("Impeccable")
        

#Retourne l'username de l'utilisateur actuel
@app.route('/', methods=['POST']) 
def get_actual_user(): 
                                                                
    if request.method == 'POST':

        if(actual_user_db.exists("actual") == 1):
            #Récupération de l'utilisateur
            actual_user = str(actual_user_db.get("actual"))
        else:
            actual_user = "invité"

        return jsonify(actual_user)
    

#Construction de l'app
if __name__ == '__main__':
    if(len(sys.argv)>1):
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("YA UN PROBLEME")
            exit(1)
    app.run(debug=True)
    

