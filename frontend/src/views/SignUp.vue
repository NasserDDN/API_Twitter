<template>

    <div id="inscription">
    
        <label for="usernameArea">Inscription</label>

        <!-- Zones des inputs de l'utilisateur -->
        <input type="text" id="usernameArea" rows = "1" cols = "20" maxlength="30" ref="username" required placeholder="Username"/>
        <input type="password" id="passwordArea1" rows = "1" cols = "20" maxlength="30" ref="password1" required placeholder="Password"/>
        <input type="password" id="passwordArea2" rows = "1" cols = "20" maxlength="30" ref="password2" required placeholder="Password confirmation"/>
    
        <!-- Bouton -->
        <input @click="SignUp" type = "submit" value = "S'inscrire" />

        <!-- Message si erreur -->
        <p ref="error" style="color: red;">{{ error_message }}</p>
    
    </div>
    
    
    
</template>
    
<script>

import axios from 'axios';
import router from '@/router';

const ax=axios.create({baseURL:'http://127.0.0.1:5000'})
    
export default {
  name: 'SignUp',

  data() {
    return {
      error_message: "",
      
    }
    
  },
  methods: {
    
        
    
    SignUp() {
    
      //Récupération des inputs
      var username = this.$refs.username.value.toString();
      var password1 = this.$refs.password1.value.toString();
      var password2 = this.$refs.password2.value.toString();

      //Vérifier que les mots de passes sont identiques
      if(password1 == password2){

        //Dictionnaire qui va être passé en paramètre de la requête
        var object = {"username": username, "password": password1, "requestType": "signup" };
    
        //Requête d'inscription
        ax.put(
            '/inscription'
            , object)
        .then((res) => {
            console.log(res);
            var data = res.data;
            console.log(data);

            this.error_message = "";

            //Si retour d'un message d'erreur
            if(data == "ERROR CODE 1"){

                this.error_message = "Pseudo déjà pris...d-_-b"

            }
            //Si tout est ok
            else{

              //Direction page de connexion
                router.push('/signIn')
            }
        })
        .catch((err) => console.log(err));

      }
      //Message d'erreur si les mots de passe sont différents
      else {
        this.error_message = "Les mots de passe doivent être identiques"
      }
    
          
    }
    
  },
  beforeMount(){

    //Modification de la classe pour la beauté de la barre de nav
    document.getElementById("routeSignUp").setAttribute("class", "routeActive");

  },
  //Avant de quitter la page
  beforeUnmount(){

    //ReModification de la classe
    document.getElementById("routeTweets").setAttribute("class", "route");
  }
}
    
</script>
    
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    
    #inscription {
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