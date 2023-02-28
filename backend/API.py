from flask import Flask
from flask import request
import sys
import json #Pour sauvegarder des dictionnaires dans les redis
import csv
import datetime
import redis



tweets_db = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True, db=0)
users_db = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True, db=1)
app = Flask(__name__)

#Supprimer toutes les keys dans le redis
#tweets_db.flushall()




#Enregistrer un tweet
#appel dans un autre terminal avec : curl -X POST http://127.0.0.1:5000/author/tweet
@app.route("/<author>/<tweet>", methods=['POST']) 
def operation(author=None, tweet=None):                                                                

    if request.method == 'POST': 

        author = str(author)
        tweet = str(tweet)

        #Création du dictionnaire
        dict = {"author":author, "tweet":tweet}
        

        #Récupération du timestamp
        current_time = datetime.datetime.now().timestamp()

        #Enregistre le tweet au timestamp actuel
        tweets_db.hmset(current_time, dict)

        #Attribut le tweet à l'utilisateur
        #Si l'utilisateur a déjà des tweets enregistrés
        if users_db.exists(author):
            print("EXISTE")
            users_db.rpush(author, current_time)
        
        #Sinon création d'une liste dans le redis
        else:
            print("EXISTE PAS")
            users_db.rpush(author, current_time)
        
        for item in users_db.lrange(author, 0 , -1):
            print(item)
        

        """
        #Conversion du float timestamp en vrai date
        date_time = datetime.datetime.fromtimestamp(current_time)
        str_date_time = date_time.strftime("%d %B %Y à %H:%M:%S")
        """

        return "Tweet enregistré, timestamp =" + str(current_time)
       
        


#Afficher tous les tweets
#appel dans un autre terminal avec : curl -X GET http://127.0.0.1:5000
@app.route("/", methods=['GET']) 
def afficher_tweets():   
    if request.method == 'GET': 

        affich = ""

        keys = tweets_db.keys()
        print(keys)

        #affich = users_db.get('nasser')

        """
        for key in keys :
        """
        key = 1677625877.41326
        value = tweets_db.hgetall(key)
        affich += value["author"] + "\n" + value["tweet"]
        

        return affich









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

"""



id_compteur = 0
dict_resultat = {}




#Calcul d'une opération 
#appel dans un autre terminal avec : curl -X POST http://127.0.0.1:5000/nom/solde
@app.route("/<nombre1>/<operation>/<nombre2>", methods=['POST']) 
def operation(operation=None, nombre1=None, nombre2=None):                                                                

    if request.method == 'POST':  

        global r

        global id_compteur

        #Récupération du compteur dans le redis
        id_compteur = int(r.get('id'))

        affich = ""

        res = 0

        operation = str(operation)
        nombre1 = int(nombre1)
        nombre2 = int(nombre2)

        if(operation == "add") :

            res = nombre1 + nombre2
            #dict_resultat[id_compteur] = res
        
        elif(operation == "sub"):

            res = nombre1 - nombre2
            #dict_resultat[id_compteur] = res
            
        elif(operation == "mul"):

            res = nombre1 * nombre2
            #dict_resultat[id_compteur] = res
        
        elif(operation == "div"):

            res = nombre1 / nombre2
            #dict_resultat[id_compteur] = res
        
        

        affich = "L'id de l'opération est " + str(id_compteur)

        #Enregistrement dans le redis
        r.set(id_compteur, res)
        
        #Incrémentation de l'id
        id_compteur += 1
        r.set('id', id_compteur)

        
        return affich

#Calcul d'une opération 
#appel dans un autre terminal avec : curl -X GET http://127.0.0.1:5000/nom/solde
@app.route("/<id>", methods=['GET']) 
def afficheResultat(id=None):  

     if request.method == 'GET':  

        #Anciennes parties du code
        #global dict_resultat
        #id = int(id)
        #res = dict_resultat[id]
        #affiche = "Le résultat est " + str(res)
        
        
        global r
        res = str(r.get(str(id)))
        affiche = "Le résultat est " + r.get(str(id))

        return affiche
        

#Affichage des keys dans le redis
print(r.keys("*"))




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


"""

"""
dict_personne= {}
dict_transac={}



##################################################################################################################################################
#Création des classes
##################################################################################################################################################
class Personne:
    def __init__(self, nom, solde):
        self.nom = nom
        self.solde = int(solde)
    
    def printPersonne(self):
        return (self.nom + " a un solde de : "+str(self.solde) + " € " + "\n")

    def getSolde(self) -> str:
        return str(self.solde)

    def setSoldePlus(self,montant):
        self.solde = self.solde + montant
    
    def setSoldeMoins(self,montant):
        self.solde = self.solde - montant
    
    def getNom(self) -> str:
        return str(self.nom)


class Transaction:
    def __init__(self, P1, P2,temps,montant):
        self.P1 = P1
        self.P2 = P2
        self.montant = montant
        self.temps = temps

    def getP1(self):
        return self.P1
 
    def getP2(self):
        return self.P2

    def printTransac(self):
        #Conversion du float timestamp en vrai date
        date_time = datetime.datetime.fromtimestamp(self.temps)
        str_date_time = date_time.strftime("%d %B %Y à %H:%M:%S")
        return (self.P1 + " a donné " + str(self.montant) + " € à "+ self.P2 + " le " + str_date_time + " \n")
    
    def getTemps(self):
        return self.temps


##################################################################################################################################################
#Récupération des données des fichiers csv
##################################################################################################################################################



#Lecture des fichiers csv (r pour avoir un raw string)
transaction_file = open(r"transactions.csv")
personnes_file = open(r"personnes.csv")

reader_transactions = csv.reader(transaction_file)
reader_personnes = csv.reader(personnes_file)




#Parcours du fichier csv contenant des personnes et leur solde
for row in reader_personnes:

    #Séparer les chaînes de caractères pour avoir accès aux différentes cases du csv
    newRow = row[0].split(';')

    #Création objet Personne
    p = Personne(str(newRow[0]), int(newRow[1]))

    #Ajout de la personne au dictionnaire
    dict_personne[len(dict_personne)] = p


#Parcours du fichier csv contenant des transactions
for row in reader_transactions:

    #Séparer les chaînes de caractères pour avoir accès aux différentes cases du csv
    newRow = row[0].split(';')

    #Création objet Transaction
    t = Transaction(str(newRow[0]), str(newRow[1]), int(newRow[2]), int(newRow[3]))

    #Ajout de la transaction au dictionnaire
    dict_transac[len(dict_transac)] = t


##################################################################################################################################################
#Fonctions utiles
##################################################################################################################################################


#Fonction qui tri chronologiquement le dictionnaire de transactions passé en paramètre
def triTransactions(transacs : dict):
    affich = ""
    for key in sorted(transacs, key=lambda item: transacs[item].temps):
            affich += transacs[key].printTransac()
    return affich

#Convertit un string en raw string(pour les paths des fichiers csv)
def to_raw(string : str):
    return fr"{string}"

##################################################################################################################################################
#Création des fonction de notre app Flask
##################################################################################################################################################


#Création d'une personne : 
#appel dans un autre terminal avec : curl -X PUT http://127.0.0.1:5000/nom/solde
@app.route("/<nom>/<solde>", methods=['PUT']) 
def add_personne(nom=None, solde=None):                                                                

    if request.method == 'PUT':                                                 
        nom =str(nom)                                 
        solde = int(solde)
        p1 = Personne(nom,solde)
        dict_personne[len(dict_personne)]=p1

        affiche= p1.printPersonne()
        return affiche



#Importation d'un csv contenant des transactions : 
#appel dans un autre terminal avec : curl -X PUT http://127.0.0.1:5000/filePath
@app.route("/<filePath>", methods=['PUT']) 
def add_transaction_file(filePath=None):                                                                

    if request.method == 'PUT':    
        affiche = ""                                             
        filePath = str(filePath)
        filePath = to_raw(filePath)

        #Lecture du fichier csv
        transactionFile = open(filePath)
        readerTransaction = csv.reader(transactionFile)

        #Parcours du fichier et ajout des transactions au dictionnaire
        for row in readerTransaction:

            #Séparer les chaînes de caractères pour avoir accès aux différentes cases du csv
            newRow = row[0].split(';')

            #Création objet Transaction
            t = Transaction(str(newRow[0]), str(newRow[1]), int(newRow[2]), int(newRow[3]))

            #Ajout de la transaction au dictionnaire
            dict_transac[len(dict_transac)] = t

        #Tri des transactions pour l'affichage
        affiche += triTransactions(dict_transac)

        return affiche


#Importation d'un csv contenant des personnes et leur solde : 
#appel dans un autre terminal avec : curl -X POST http://127.0.0.1:5000/filePath
@app.route("/<filePath>", methods=['POST']) 
def add_personnes_file(filePath=None):                                                                

    if request.method == 'POST':    
        affiche = "Ajout des personnes suivantes dans le registre : \n"                                             
        filePath = str(filePath)
        filePath = to_raw(filePath)

        #Lecture du fichier csv
        personnesFile = open(filePath)
        readerPersonnes = csv.reader(personnesFile)

        #Parcours du fichier et ajout des transactions au dictionnaire
        for row in readerPersonnes:

            #Séparer les chaînes de caractères pour avoir accès aux différentes cases du csv
            newRow = row[0].split(';')

            #Création objet Transaction
            p = Personne(str(newRow[0]), int(newRow[1]))

            #Ajout de la transaction au dictionnaire
            dict_personne[len(dict_personne)] = p

            #Pour afficher les nouvelles personnes du registre
            affiche += p.printPersonne()

        return affiche
        



#Affichage de toutes les transactions dans l'ordre chronologique : 
#appel dans un autre terminal avec : curl -X GET http://127.0.0.1:5000
@app.route("/", methods=['GET']) 
def affichage_transactions(): 

    if request.method == 'GET' :

        return triTransactions(dict_transac)
        


#Afficher le solde et les transactions d'une personne dans l'ordre chronologique :
#appel dans un autre terminal avec : curl -X GET http://127.0.0.1:5000/nom
@app.route("/<nom>", methods=['GET']) 
def personne_transactions(nom=None):  

    if request.method == "GET" :
        nom = str(nom)
        transactions = {}
        nb_transactions = 0
        personne_trouvee = False
        affich = ""

        #Parcours du dictionnaire de personnes pour afficher le solde de la personne
        for i in dict_personne :
            if dict_personne[i].getNom() == nom :
                affich += dict_personne[i].printPersonne()
                personne_trouvee = True
        
        if personne_trouvee == False :
            return "Personne non trouvée dans le système"

        #On cherche les transactions dans lesquelles la personne est impliquée
        for i in dict_transac:
            if (nom == dict_transac[i].getP1() or nom == dict_transac[i].getP2()):
                transactions[len(transactions)] = dict_transac[i]
                nb_transactions += 1

        if nb_transactions == 0 :
            return "Pas de transactions pour cette personne"
        
        


        affich += triTransactions(transactions)
        #Affichage des transactions triées
        return affich


#Suppression d'une personne : 
#Appel dans un aurtre terminal avec : curl -X DELETE http://127.0.0.1:5000/nom"
@app.route("/<nom>", methods=['DELETE']) 
def delete_personne(nom=None):

    if request.method == 'DELETE':
        affich = ""
        personne_trouvee = False
        
        for key, item in dict_personne.items():
            if item.getNom() == nom :
                #Suppression de la personne
                dict_personne.pop(key)
                personne_trouvee = True
                break
        
        if personne_trouvee == True :
            for item in dict_personne:
                    affich += dict_personne[item].printPersonne()

        else :
            return "Personne non trouvée dans le système"

        

        return affich
    


#Création d'une transaction : 
#appel dans un aurtre terminal avec : curl -X POST http://127.0.0.1:5000/nom1/nom2/montant"
@app.route("/<nom1>/<nom2>/<montant>", methods=['POST']) 
def ajout_transation(nom1=None,nom2=None,temps=None,montant=None):

    if request.method == 'POST':

        #Récupération des données de la commande 
        temps = datetime.datetime.now().timestamp()
        montant=int(montant)
        nom1 = str(nom1)
        nom2 = str(nom2)
        affich = ""

        #On regarde si nos personnes sont dans la base de données
        test = 0
        Per1 = 0
        Per2 = 0

        for personne in dict_personne :
            if(dict_personne[personne].getNom() == nom1):
                test = test + 1
                Per1 = personne
                
            if(dict_personne[personne].getNom() == nom2):
                test = test + 1
                Per2 = personne

        #Si non => ERREUR    
        if test != 2 :
            affich = "Echec Transac" + "\n"

            return affich

        #Si oui on procede à la transaction   
        else :
            t1=Transaction(nom1,nom2,temps,montant)
            
            #Modification des soldes
            dict_personne[Per1].setSoldeMoins(montant)
            dict_personne[Per2].setSoldePlus(montant)

            dict_transac[len(dict_transac)]=t1
            affich = str(dict_transac[len(dict_transac)-1].printTransac())

            return affich

"""


