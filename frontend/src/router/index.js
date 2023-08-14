import { createRouter, createWebHashHistory } from 'vue-router'

import HomeView from '@/views/HomeView'
import FlashCards from '@/views/FlashCards'
import DashView from '@/views/DashView'
import LoginView from '@/views/LoginView'
import NotesView from '@/views/NotesView'
import QuizzesView from '@/views/QuizzesView'
const routes = [

  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: function () {
  //     return import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  //   }
  // }
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashView
  },
  {
    path: '/flashcards',
    name: 'Flashcards',
    component: FlashCards
  },
  {
    path: '/notes',
    name: 'Notes',
    component: NotesView
  },
  {
    path: '/quizzes',
    name: 'Quizzes',
    component: QuizzesView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
