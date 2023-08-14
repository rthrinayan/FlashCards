const axios = require('axios')

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'token': document.cookie.split(';')[0]
    }
})

const card = {
    state: {
        cards: []
    },

    getters: {
        getCards: (state) => state.cards,

        getCardById: (state) => (id) => {
            return state.cards.find(card => card.id === id)
        }
    },

    mutations: {
        setCards(state, payload) {
            state.cards = []
            state.cards = payload
        },

        addCard(state, payload) {
            if (state.cards.find(card => card.id === payload.id)) return;
            state.cards.push(payload)
        },

        deleteCard(state, id) {
            state.cards = state.cards.filter(card => {
                return !(card.id === id)
            })
        },

        updateCard(state, { payload, id }) {
            let modCard = state.cards.find(card => card.id === id)
            state.cards = state.cards.filter(card => card.id !== id)
            modCard.front = payload.front;
            modCard.back = payload.back;
            state.cards.push(modCard)
        }
    },

    actions: {
        async GetCards(context, did) {
            let res = await axiosInstance.get('deck/card/' + did)
            if (res.status === 200) {
                context.commit('setCards', res.data)
                console.log(res.data)
            } else {
                console.log('Error' + res.data)
            }
        },

    }
}