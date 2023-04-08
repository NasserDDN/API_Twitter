<template>

<div class="tweetDiv">

        <div style="font-weight: bold; margin-bottom: 10px;flex-direction: row;" n>
            <img @click="UserPage" alt="Photo de profil" src="../assets/photoDeProfil.png" width="30" height="30" style="vertical-align: middle;"> <span id="username" @click="UserPage">{{ author }} </span>  
            &nbsp;<span style="font-weight:1; color: gray; font-size: medium;">{{time}}</span>
            
        </div>
        <p>{{ tweet }}</p>

        <input @click="Retweet" type = "submit" value = "Retweet" class="retweet_btn" />

    </div>

</template>

<script>
import router from '@/router';
import axios from 'axios';

//Pour les requêtes
const ax=axios.create({baseURL:'http://127.0.0.1:5000'});

export default {
    name: 'Tweet',
    data(){
        return {
            user: String,
        }
        
    },
    //Déclaration des paramètres que la page reçoit
    props: {

        author: {
            default: "No Author"

        },
        tweet: {
            default: "No Tweet"
        },
        time: {
            default: "No Time"
        },
        id:{
            default: 0
        }
        

    },
    methods: {

        async Retweet(){

            //Requete pour savoir qui est l'utilisateur qui veut retweeter
            await ax.post('/')
            .then((res) => {
                console.log(res);
                var data = res.data;
                
                //Modification de l'utilisateur actuel
                this.user = data.toString();

            })
            .catch((err) => console.log(err));

            //Un invité ne peut pas retweeter
            if(this.user == "invité"){
                this.error_message = "Connectez vous pour pouvoir retweeter";
            }
            else{

                //Paramètre de la requête
                var object = {"user": this.user,"author_of_tweet": this.author, "id": this.id, "requestType": "retweet"};

                //Requête Retweet
                ax.put(
                    '/inscription'
                    , object)
                .then((res) => {
                    console.log(res);
                    var data = res.data;
                    console.log(data);

                })
                .catch((err) => console.log(err));
            }

        },

        UserPage(){
            router.push({name: 'userpage', params: {user: this.author}})
        }

    }
}

</script>


<style>

.tweetDiv{
  margin: 5px 30px 5px 30px ;

  display: flex;

  align-items: start;

  flex-direction: column;
}

img:hover {

    color: rgb(64, 151, 204);
    font-weight: bold;
    cursor: pointer;

}

#username:hover {
    cursor: pointer;
}

input {
    background-color: rgb(240, 248, 255);
    border-radius: 7px;
    

}

input:hover {
    cursor: pointer;
    background-color: rgb(118, 191, 255);
    color: white;


}

.retweet_btn {
    background-color: rgb(222, 220, 220);
}

</style>