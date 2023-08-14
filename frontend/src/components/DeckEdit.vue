<template>
    <div class="input-group input-group-sm mb-3">
        <div style="width:100%">
            <input type="text" class="form-control" placeholder="Name" aria-describedby="basic-addon1" v-model="name"
                style="text-align:center">
        </div>
        <br>

        <br>
        <div style="width:100%">
            <textarea class="form-control" placeholder="Description" aria-label="Description" v-model="description"
                style="text-align:center"></textarea>
        </div>
        <div style="margin-top:1rem; margin-right:20%; margin-left:20%">
            <input type="color" class="form-control form-control-color" id="exampleColorInput" title="Choose your color"
                v-model="colour">
        </div>

        <div class="d-grid gap-0" style="justify-content: center;">
            <button type="button" class="btn btn-outline-primary" v-on:click="onSubmit()"
                style="width:100%">Edit</button>
        </div>
    </div>
    {{ colour }}
</template> 

<script>
import { mapActions } from 'vuex'
export default {
    name: 'DeckEdit',
    data() {
        return {
            name: '',
            description: '',
            colour: '',
        }
    },
    props: ['deckObj'],
    methods: {
        ...mapActions({
            UpdateDeck: 'UpdateDeck'
        }),
        onSubmit() {
            this.UpdateDeck({
                id: this.deckObj.id,
                payload: {
                    'name': this.name,
                    'description': this.description,
                    'colour': this.colour
                }
            })
            this.$emit('edited-deck')
        }
    },
    mounted() {
        this.name = this.deckObj.name
        this.description = this.deckObj.description
    },
    emits: ['edited-deck']
}
</script>
