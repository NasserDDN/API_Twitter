<template>
    <!-- Division qui contient la liste des tweets -->
    <div id="all_tweets">
      
        <!-- Liste de components "Tweet" -->
        <ol id="v-for-listTweets" class="listOfTweets">
            <li v-for="tweet in listTweets" :key="tweet.id" class="aTweet">
                <Tweet :author="tweet.author" :tweet="tweet.tweet" :time="tweet.time"/>
            </li>
        </ol>

    </div>
  
</template>

<script>
import axios from 'axios';
import Tweet from '../components/Tweet.vue'


const ax=axios.create({baseURL:'http://127.0.0.1:5000'})

export default {
    name: 'Profil',
    components: {

        Tweet,

    },
    //Déclaration de la variable que va recevoir la page
    props: {

        sujet: String

    },
    data() {
        return {

            listTweets: [{ author: "None", tweet: "Pas de tweet"}],
      
        }
    },
    methods: {

        //Requête pour mettre à jour la liste des tweets liés au sujet
        AffichTweets() {

            //Ajout du -h pour préciser que nous voulons tous les tweets d'un sujet
            var value = "h-" + this.sujet;

            //Paramètre
            var object = {data: value.toString()}

            ax.put('/'
            ,object
            )
            .then((res) => {
                console.log(res.data);
                var data = res.data;

                //Récupération des tweets
                //eslint-disable-next-line
                this.listTweets = data;
            })
            .catch((err) => console.log(err));

        },

    },
    //Requête pour afficher les tweets avant l'affichage de la page
    beforeMount() {
        this.AffichTweets();
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



