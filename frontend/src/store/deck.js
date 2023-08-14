const axios = require('axios')

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'token': document.cookie.split(';')[1]
    }
})

const deck = {
    state: {
        decks: []
    },

    getters: {
        getSortedDecks: (state) => {
            return state.sort((a, b) => {
                (a.created > b.created) ? 1 : ((b.created > a.created) ? -1 : 0)
            })
        },
        getDecks: (state) => {
            return state.decks
        },
        getDeckById: (state) => (id) => {
            return state.decks.find(deck => deck.id === id)
        }
    },

    mutations: {
        setDecks(state, payload) {
            state.decks = []
            state.decks = payload
        },
        addDecks(state, payload) {
            if (state.decks.find(deck => deck.id === payload.id)) return
            state.decks.push(payload)
        },
        deleteDeck(state, id) {
            state.decks = state.decks.filter((deck) => {
                return !(deck.id === id)
            })
        },
        updateDeck(state, { payload, id }) {
            let modDeck = state.decks.find(deck => deck.id === id)
            state.decks = state.decks.filter(deck => deck.id !== id)
            modDeck.name = payload.name
            modDeck.description = payload.description
            state.decks.push(modDeck)
        }

    },

    actions: {
        async GetDecks(context) {
            console.log(document.cookie)
            let res = await axiosInstance.get('user/deck')
            if (res.status === 200) {
                context.commit('setDecks', res.data)
                console.log(res.data)
            } else {
                console.log('Error' + res.data)
            }
        },

        async DeleteDeck(context, id) {
            let res = await axiosInstance.delete('deck/' + id)
            console.log('Deleting deck : ', id)
            if (res.status === 200) {
                context.commit('deleteDeck', id)
                console.log(res.data)
            } else {
                console.log('Error : ', res.data)
            }
        },

        async UpdateDeck(context, { id, payload }) {
            console.log('Updating deck : ', id, 'to', payload)
            let res = await axiosInstance.patch('deck/' + id, payload)
            if (res.status === 200) {
                context.commit('updateDeck', { id: id, payload: payload })
            } else {
                console.log(res.data)
            }
        },

        async AddDeck(context, formData) {
            console.log(formData)
            let res = await axiosInstance.post('deck',
                {
                    'name': formData.name,
                    'description': formData.description,
                    'colour': formData.colour
                })

            if (res.status === 200) {
                console.log(res.data)
                let resGet = await axiosInstance.get('deck/' + res.data.did)
                if (resGet.status === 200) {
                    context.commit('addDecks', resGet.data)
                } else {
                    console.log(resGet.data)
                }
            } else {
                console.log(res.data)
            }
        }
    }
}

export default deck 