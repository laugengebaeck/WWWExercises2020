import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'

import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.component('icon', Icon)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
