<script>
import router from '@/router';
import axios from 'axios';
import Tweet from '../components/Tweet.vue'

const ax=axios.create({baseURL:'http://127.0.0.1:5000'})

export default {
  name: 'ShowTweets',
  components: {
    Tweet,
    
  },
  data() {
    return {

      //Listes des tweets et des sujets
      listTweets: [{ author: "None", tweet: "Pas de tweet"}],
      listHashtags: ["Pas de sujets"],

      //Utilisateur actuellement connecté
      user: {
        default: "invité"
      },
      error_message: ""
      
    }
    
  },
  methods: {
    
    //Requête pour enregistrer un tweet
    async SaveTweet () {

      //Si l'utilisateur n'est pas connecté
      if(this.user == "invité"){
        this.error_message = "Connectez-vous ou créer un compte pour publier un tweet"
      }
      //Si il est connecté
      else{

        //Récupération du tweet dans la zone de texte
        var the_tweet = this.$refs.newTweet.value.toString();

        //Paramètre
        var object = { author: this.user.toString(), tweet: the_tweet };

        //Requête
        await ax.post(
          '/postTweet'
          , object)
        .then((res) => {
          console.log(res);
          var data = res.data;
          console.log(data);
        })
        .catch((err) => console.log(err));


        //Mise à jour de la liste des tweets
        this.AffichTweets();
      }
    },

    //Requête pour récupérer l'username de l'utilisateur actuel
    GetActualUser(){

      ax.post('/')
      .then((res) => {
      console.log(res);
      var data = res.data;
      
      //Récupération de l'username
      this.user = data.toString();

      })
      .catch((err) => console.log(err));

    },



      

      /*
      { transformRequest: [(data, headers) => {
          delete headers.common['X-Requested-With'];
          return data 
        }] })
      */
    
    

    //Requête pour récupérer la liste des tweets
    //Ainsi que la list des sujets
    AffichTweets () {

      //Requête pour l'affichage des tweets
      ax.get('/')
      .then((res) => {
        console.log(res.data);
        var data = res.data;

        //Modification des listes de tweets et de sujets
        //(Pour éviter les warnings inutiles) =>
        //eslint-disable-next-line
        this.listTweets = data["tweets"];
        this.listHashtags = data["sujets"];
        
        
      })
      .catch((err) => console.log(err));

    },

    //Méthode pour rédiriger vers la page affichant les tweets liés à un sujet
    Sujet(hashtag){
      router.push({name: 'sujet', params:{sujet: hashtag}});
    },
    
  },
  //Avant l'affichage de la page
  beforeMount() {
    this.GetActualUser();
    this.AffichTweets();
    
    //Modification de la classe pour la beauté de la barre de nav
    document.getElementById("routeTweets").setAttribute("class", "routeActive");

  },
  //Avant de quitter la page
  beforeUnmount(){

    //ReModification de la classe
    document.getElementById("routeTweets").setAttribute("class", "route");
  }
}
</script>


<template>

  <div id="this_page">

  
    <!-- Division concernant l'affichage et la publication des tweets -->
    <div id="partie_tweets">

      <!-- Division pour publier un tweet -->
      <p>Connecté(e) en tant que <span style="font-size: large; font-weight: bold; background-color:  rgb(240, 248, 255); border-radius: 5px; padding: 1%;">{{ user }}</span></p>
      <div id="post_tweet">
        <label for="tweetArea">Entrez un tweet</label>
        <textarea id="tweetArea" rows = "5" cols = "60" maxlength="280" ref="newTweet" placeholder="Ecrire un tweet" style="resize: none;"></textarea>
        <input @click="SaveTweet" type = "submit" value = "Tweeter" />
        <p ref="error" style="color: red;">{{ error_message }}</p>
      </div>

    <!-- Division qui contient la liste des tweets -->
    <div id="all_tweets">
      <!-- Liste de components "Tweet" -->
      <ol id="v-for-listTweets" class="listOfTweets">
      <li v-for="tweet in listTweets" :key="tweet.id" class="aTweet">
        <Tweet :author="tweet.author" :tweet="tweet.tweet" :time="tweet.time" :id="tweet.id"/>
      </li>
    </ol>
    </div>

    </div>
    

    <!-- Division qui contient la liste des sujets -->
    <div id="partie_sujets">
      <h3 style="font-size: large; font-weight: bold; background-color:  rgb(240, 248, 255); border-radius: 5px; padding: 5%;">SUJETS</h3>
      <ol id="v-for-listHashtags" class="listOfHashtags">
      <li @click="Sujet(hashtag)" v-for="hashtag in listHashtags" :key="hashtag.id" class="one_hashtag" >
        {{hashtag}}
      </li>
    </ol>
    </div>

  </div>


</template>

<style>
#post_tweet {
    display: flex;

    justify-content: center;

    flex-direction: column;

    margin: 2%;
}

#all_tweets {
    display: flex;

    justify-content: center;

    flex-direction: column;
}

#partie_sujet {

    display: flex;

    justify-content: center;

    flex-direction: column;

}

#this_page {

  width: 100%;
  display: flex;

  justify-content: space-around;
}

ol {
  list-style-type: none;

  padding: 0%;
  margin: 0%;
  border: 0;

}

.one_hashtag {
  margin-top: 5%;
  margin-bottom: 5%;
}

.one_hashtag:hover {
  font-weight: bold;
  cursor: pointer;
  border-radius: 5%;
  background-color: rgb(118, 191, 255);
  color: white;
  border-radius: 5px;
}

.aTweet {
  background-color: rgb(240, 248, 255);

  border-radius: 10px;
}


</style>