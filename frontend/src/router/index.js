import { createRouter, createWebHistory } from 'vue-router'
import SignIn from '@/views/SignIn.vue'
import Tweets from '@/views/Tweets.vue'
import SignUp from '@/views/SignUp.vue'
import Profil from '@/views/Profil.vue'
import Sujet from '@/views/Sujet.vue'
import UserPage from '@/views/UserPage.vue'

//Déclaration des routes
const routes = [
  //Page de l'utilisateur connecté
  {
    path: '/profil',
    name: 'profil',
    component: Profil,
  },
  //Page de connexion
  {
    path: '/signIn',
    name: 'signIn',
    component: SignIn
  },
  //Page d'accueil où sont affichés tous les tweets
  {
    path: '/',
    name: 'tweets',
    component: Tweets,
  },
  //Page d'inscription
  {
    path: '/signUp',
    name: 'signUp',
    component: SignUp
  },
  //Page contenant les tweets liés à un sujet
  {
    path: '/:sujet',
    name: 'sujet',
    component: Sujet,
    props: true
  },
  //Page du profil d'un autre utilisateur (pas celui connecté)
  {
    path: '/:user',
    name: 'userpage',
    component: UserPage,
    props: true
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
