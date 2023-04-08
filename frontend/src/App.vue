

<template>
  <header>
    <div style="text-align: center; vertical-align: text-bottom;">
      <img alt="Vue logo" src="./assets/logo.png" width="150" height="130" />
      <div id="nav">
        <!-- Routes pour aller sur d'autres pages -->
      <RouterLink class="route" id="routeSignUp" to="/signUp">Inscription</RouterLink> &nbsp;
      <RouterLink class="route" id="routeSignIn" to="/signIn">Connexion</RouterLink> &nbsp;
      <RouterLink class="route" id="routeTweets" ref="routeTweetsRef" to="/">Tweets</RouterLink> &nbsp;
      <RouterLink class="route" id="routeProfil" to="/profil">Profil</RouterLink>
      </div>
    </div> 
  </header>


  <div id="mainContent">
    <RouterView />
  </div>



</template>

<script>

export default {
  name: 'App'
}
</script>

<style>

#nav {
  justify-self: end;

  margin: 1%;

  padding: 0.3%;
}

body {
    margin: 0;
    padding: 0;
} 

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

header {
  background-color: rgb(146, 225, 249);

}

#mainContent {
  display: flex;

  flex-direction: column;

  align-items: center;
}

.route {

  text-decoration: none;
  color: black;
  font-size: large;

  
  padding: 5px;
  
}

.route:hover, .routeActive {
  text-decoration: none;
  color: black;
  font-size: large;
  padding: 5px;
  
  background-color: rgb(215, 233, 250);
  border-radius: 1px;
}



</style>
