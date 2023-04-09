<template>

<div id="connexion">

    <label for="usernameArea">Connexion</label>

    <input type="text" id="usernameArea" rows = "1" cols = "20" maxlength="30" ref="username" required placeholder="Username"/>
    
    <input type="password" id="passwordArea" rows = "1" cols = "20" maxlength="30" ref="password" required placeholder="Password"/>

    <input @click="SignIn" type = "submit" value = "Connexion" />

    <input @click="Invite" type = "submit" value = "Continuer en tant qu'invité" />

    <p ref="error" style="color: red;">{{ error_message }}</p>

  </div>



</template>

<script>

import router from '@/router';
import axios from 'axios';


const ax=axios.create({baseURL:'http://127.0.0.1:5000'})

export default {
  name: 'SignIn',

  data() {
        return {
            error_message: "",
      
        }
    
    },
  methods: {

    //Connexion en tant qu'invité
    Invite(){

      //Paramètre
      var object = {"username": "invité", "password": "invité", "requestType": "signin"};

      //Requête de connexion
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
    },

    

    //Connexion
    SignIn() {

      //Récupération de l'identifiant et du mot de passe
      var username = this.$refs.username.value.toString();
      var password = this.$refs.password.value.toString();

      //Paramètre
      var object = {"username": username, "password": password, "requestType": "signin"};

      //Requête de connexion
      ax.put(
        '/inscription'
        , object)
      .then((res) => {
        console.log(res);
        var data = res.data;

        //Message si la connexion a échoué
        if(data == "ERROR CODE 1"){
          this.error_message = "Mot de passe incorrect...d-_-b"
        }
        else if(data == "ERROR CODE 2"){
          this.error_message = "Ce pseudo n'existe pas...d-_-b"
        }
        //Si connexion a réussie
        else {
          //Direction page du profil
          router.push('/profil');
        }

      })
      .catch((err) => console.log(err));

    
    }

  },
  beforeMount(){

    //Modification de la classe pour la beauté de la barre de nav
    document.getElementById("routeSignIn").setAttribute("class", "routeActive");

  },
  //Avant de quitter la page
  beforeUnmount(){

    //ReModification de la classe
    document.getElementById("routeTweets").setAttribute("class", "route");
  }
}

</script>


<style scoped>

#connexion {
  display: flex;
  justify-content: space-between;
  width: 20%;
  height: 200px;
  flex-direction: column;

  margin: 2%;

  padding: 1%;

  background-color: rgb(221, 228, 245);

  border-radius: 10px;
}

input {
  height: 10%;
}

</style>