import { createStore } from 'vuex'

import authentication from '@/store/authentication'
import deck from '@/store/deck'

export default createStore({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    authentication: authentication,
    deck: deck
  }
})
