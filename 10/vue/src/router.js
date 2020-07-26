import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'Home',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Home.vue')
    },
    {
      path: '/questions',
      name: 'Questions',
      component: () => import(/* webpackChunkName: "about" */ './views/Questions.vue')
    },
    {
      path: '/api',
      name: 'API',
      component: () => import(/* webpackChunkName: "about" */ './views/API.vue')
    }
  ]
})
