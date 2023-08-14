<template>
    <div class="row">


        <div v-for="(deck, index) in this.$store.state.deck.decks" v-bind:key="deck.id" class='column'>

            <div class="card mx-5 " style="width:rem; background-color: whitesmoke">
                <div class="card-body" style="background-colour:{{deck.colour}}">
                    <h3 class="card-title">{{ deck.name }}</h3>
                    <h6 class="card-subtitle mb-2 text-muted">Score : {{ deck.deck_score ? deck.deck_score : 0 }}</h6>
                    <p class="card-text" v-on:mouseover="this.showOptions[index] = true"
                        v-on:mouseleave="this.showOptions[index] = false" style="">{{ deck.description }}
                    <ul class="list-group" v-show="this.showOptions[index]">
                        <li class="list-group-item d-grid gap-2">
                            <button type="button" class="btn btn-outline-success" v-on:click="">
                                View
                            </button>
                        </li>
                        <li class="list-group-item d-grid gap-2">
                            <button type="button" class="btn btn-outline-primary dropdown-toggle"
                                data-bs-toggle="collapse" data-bs-target="#collapseExample" aria-expanded="false"
                                aria-controls="collapseExample">Edit</button>
                        </li>
                        <li class="list-group-item d-grid gap-2">
                            <button type="button" class="btn btn-outline-danger" v-on:click="DeleteDeck(deck.id)">Delete
                            </button>
                        </li>
                    </ul>
                    </p>
                </div>
                <div class="collapse" id="collapseExample">
                    <div class="card card-body">
                        <DeckEdit v-bind:deckObj="deck" @edited-deck="clickEdit()"></DeckEdit>
                    </div>
                </div>
            </div>
            <br>
        </div>

        <AddDeck></AddDeck>

    </div>

</template>

<script>
import { mapActions } from 'vuex'
import { mapGetters } from 'vuex'
import { mapState } from 'vuex'
import DeckEdit from '@/components/DeckEdit.vue'
import AddDeck from '@/components/AddDeck.vue'
export default {
    name: 'FlashCards',
    data() {
        return {
            showOptions: [],
            showEdit: false
        }
    },
    methods: {
        ...mapActions({
            GetDecks: 'GetDecks',
            DeleteDeck: 'DeleteDeck',
            UpdateDeck: 'UpdateDeck'
        }),
        toggleOptions() {
            this.showOptions = true;
        },
        clickEdit() {

        }
    },
    mounted() {
        this.GetDecks()
        for (let i = 0; i < this.$store.state.deck.decks.length; i++) this.showOptions.push(false)
            // ('.toast').show('show')
    },
    computed: {
        ...mapGetters({ getDecks: 'getDecks' }),
        ...mapState({ decks: 'deck/decks' })
    },
    components: {
        DeckEdit,
        AddDeck
    }
}
</script>

<style scoped = true>
* {
  box-sizing: border-box;
}

.column {
  float: left;
width: 33%;
  padding: 0 10px;
}

/* Remove extra left and right margins, due to padding */
.row {margin: 0 -5px; }

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
@media screen and (max-width: 800px) {
  .column {
    width: 50%;
    display: block;
    margin-bottom: 20px;
  }
}

@media screen and (max-width: 600px) {
    .column {
        width: 100%;
        display : block; 
        margin-bottom: 20px;
    }
}
</style>