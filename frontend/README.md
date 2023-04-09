# Frontend

Pour le frontend, j'ai utilisé le framework VueJS (VueJS 3) 
![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
qui permet de créer des interfaces utilisateurs monopages.

Une page classique est composé de 3 balises :
* `<template>` : partie html
* `<script>`: partie JavaScript
* `<style>`: partie CSS

Une des forces de `VueJS` est que les pages sont dynamiques : si une modification est faite, la page se mettra à jour automatiquement => pas besoin de recharger la page à chaque fois comme en `HTML/CSS`.



## Composition du frontend

Il est composé du fichier `App.vue`qui est la page affichée lorsque l'on va à l'adresse [localhost:8000](http://127.0.0.1:8000/) ou [localhost:8080](http://127.0.0.1:8080/) (si vous n'avez pas utilisé les conteneurs).

Il y a ensuite les différentes pages :
* `Tweets.vue`: affiche le contenu de la page d'accueil
* `Profil.vue`: affiche la page de l'utilisateur (ses tweets ainsi que les tweets qu'il a retweeté) actuellement connecté
* `SignIn.vue`: la page de connexion
* `SignUp.vue`: la page d'inscription
* `Sujet`: affiche les tweets liés à un sujet
* `UserPage.vue`: affiche la page d'un utilisateur quelconque (après un clic sur le pseudo ou la photo de profil d'un utilisateur)

Il y a un fichier `Tweet.vue` dans le dossier `components`. On peut définir ce fichier comme une classe dans les langages de programmation orientés objet (C++ par exemple). Ce fichier est donc la "classe" d'un tweet. Lorsque ce composant `Tweet.vue` sera appelé dans une autre page, des variables lui seront passées en paramètre pour qu'un tweet puisse être affiché.

Il y a un fichier `main.js` à la racine du dossier frontend. Ce fichier sert à créer l'App VueJs et à importer des modules ou librairies. Dans ce fichier, on voit que l'application utilise 2 librairies: `axios` et `router`.



### Axios

Axios est un client HTTP basé sur des promesses permettant de faire des requêtes à notre API Flask. Grâce à ce client, nous pouvons faire des requêtes et y inclure des paramètres. Les données passées en paramètres sont automatiquement converties en objet JSON: c'est très pratique pour pouvoir envoyer tout type de données à notre API.



### Router (version 4: adaptée à la version 3 de VueJS)

Router est un projet open source qui fait partie de lécosystème de VueJS. Router permet de pouvoir facilement naviguer entre les pages de notre application (lors d'un événement par exemple). 

Pour pouvoir naviguer entre les pages, il faut définir des chemins (ou route) dans le fichier `router/index.js` de cette façon :

```
{
  path: '/nom_du_chemin' ou '/nom_du_chemin/:parametre' si nous voulons passer une variable en paramètre,
  name: 'nom pour accéder plus facilement à cette route'
  component: La destination de cette route,
  props: true (si nous voulons passer une variable en paramètre)
}

```

Il y a 2 manières de naviguer entre les pages :

* J'utilise la première sur la page principale du projet `App.vue`:

  Il y a des balises `<RouterLink>` ainsi qu'une balise `<RouterView>`. 

  Les balises `RouterLink` sont des liens vers d'autres pages de l'App. Un attribut `to="/route"` est insérer dans cette balise pour spécifier la page de destination.

  La balise `RouterView` est l'endroit où va être affiché la page : lorsque l'utilisateur clique sur un RouterLink, le contenu de la page de destination sera affiché à   cet endroit à chaque fois. 

  Les balises `RouterLink` sont dans le header et le `RouterView` est dans une div à l'extérieur. Cela permet d'avoir un header fixe dans l'App sans avoir besoin de     copier coller le code du header dans chaque page.

  Dans notre cas, on peut considérer le `App.vue` comme la page parent et les autres pages comme des pages enfants.

  Si on veut aller à une page enfant depuis une page enfant, il faut utiliser la seconde façon de naviguer.
  

* J'utilise cette deuxième manière dans les pages enfants lorsque c'est nécessaire après un event :
  
  Sans paramètre :
  ```
  router.push('chemin_de_la_page')
  ```
  
  Avec paramètre :
  ```
  router.push({name: 'nom_de_la_page', param: {nom_du_paramètre_indiqué_dans_le_chemin: variable}})
  ```
  
  Je ne vais pas expliquer le code en détail : il est documenté et un fichier VueJS est facile à comprendre si on connaît les langages HTML, CSS et Javascript
  

  
  




