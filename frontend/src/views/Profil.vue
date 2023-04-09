<template>
    <input type = "submit" value = "Déconnexion" ref="disconnectBtn" v-bind:style="{ display: computedDisplay }" @click="Disconnect"/>
    <!-- Division qui contient la liste des tweets -->
    <div id="all_tweets">
      
      <!-- Liste de components "Tweet" -->
      <ol id="v-for-listTweets" class="listOfTweets">
      <li v-for="tweet in listTweets" :key="tweet.id" class="aTweet">
        <Tweet :author="tweet.author" :tweet="tweet.tweet" :time="tweet.time"/>
      </li>
    </ol>
    <p>{{ message }}</p>
    </div>
  
  
</template>

<script>
import router from '@/router';
import axios from 'axios';
import Tweet from '../components/Tweet.vue'

//Pour les requêtes
const ax=axios.create({baseURL:'http://127.0.0.1:5000'})

export default {
  name: 'Profil',
  components: {
    Tweet,
  },
  data() {
    return {
      listTweets: [{ author: "None", tweet: "Pas de tweet"}],

      //Utilisateur actuel
      user: String,

      //Display du bouton déconnexion
      display: 'block',

      message: String
      
    }
    
  },
  //Retourne la valeur de display
  //Nécessaire pour que l'affichage ou non du bouton soit en temps réel
  computed: {
    computedDisplay: function () {
      return this.display;
    }
  },
  methods: {

    //Requête pour récupérer l'username de l'utilisateur actuel
    async GetActualUser(){

      await ax.post('/')
      .then((res) => {
        console.log(res);
        var data = res.data;

        //Si l'utilisateur n'est pas connecté
        if(data == "invité"){

          //Le bouton déconnexion n'est plus affiché
          this.display = 'none';

          //Affichage d'un message
          this.message = "Connectez-vous pour publier votre premier tweet d-_-b"
        }

        //Si l'utilisateur est connecté
        else{
          this.display = 'block';
        }
        
        //Récupération de l'username
        this.user = data.toString();

      })
      .catch((err) => console.log(err));

      //Affichage des tweets
      this.AffichTweets();



    },

    //Requête pour afficher les tweets de l'utilisateur connecté
    AffichTweets () {

      //Ajout du -u pour préciser que nous voulons tous les tweets d'un utilisateur
      var value = "u-" + this.user;

      //Paramètre
      var object = {data: value.toString()}

      //Requête
      ax.put('/'
        , object
        )
      .then((res) => {
        console.log(res.data);
        var data = res.data;

        //eslint-disable-next-line
        this.listTweets = data;
      })
      .catch((err) => console.log(err));

    },

    //Déconnexion de l'utilisateur
    Disconnect(){

      //Paramètre (l'utilisateur sera connecté avec un compte invité après la déconnexion)
      var object = {"username": "invité", "password": "invité", "requestType": "signin"};

      //Requête
      ax.put(
        '/inscription'
        , object)
      .then((res) => {
        console.log(res);
        var data = res.data;
        console.log(data);

        //Retour à la page d'accueil
        router.push('/');
        
      })
      .catch((err) => console.log(err));
    }
          
  },
  //Avant l'affichage de la page
  beforeMount() {
    this.message = "";
    this.GetActualUser();

    //Modification de la classe pour la beauté de la barre de nav
    document.getElementById("routeProfil").setAttribute("class", "routeActive");

  },
  //Avant de quitter la page
  beforeUnmount(){

    //ReModification de la classe
    document.getElementById("routeTweets").setAttribute("class", "route");
  }
}
</script>

<style>

#all_tweets {
    display: flex;

    justify-content: center;

    flex-direction: column;
}

</style>


