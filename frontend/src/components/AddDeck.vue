<template>

    <div class="card mx-5" style="width: 18rem; background-color:whitesmoke;">
        <div class="card-body">
            <h3 class="card-title"> Add</h3>
            <p class="card-text">
            <div class="input-group input-group-sm mb-3">
                <div style="width:100%">
                    <input type="text" class="form-control" placeholder="Name" aria-describedby="basic-addon1"
                        v-model="deckName" style="text-align:center">
                </div>
                <br>

                <br>
                <div style="width:100%">
                    <textarea class="form-control" placeholder="Description" aria-label="Description"
                        v-model="deckDescription" style="text-align:center"></textarea>
                </div>
                <div style="margin-top:1rem;  margin-left:40%">
                    <input type="color" class="form-control form-control-color" id="exampleColorInput"
                        title="Choose your color" v-model="deckColour">
                </div>
                <div>
                    <br>
                    Import using CSV
                    <form id="uploadForm" enctype="multipart/form-data" v-on:change="uploadFile">
                        <input class='form-control' type="file" id="file" name="file">
                    </form>
                    <button type="button" class="btn btn-outline-success" v-on:click="onSubmit()">Add</button>
                </div>
            </div>
            </p>
        </div>
    </div>

</template>

<script>
import { mapActions } from 'vuex'
const axios = require('axios')

export default {
    name: 'AddDeck',
    data() {
        return {
            deckName: '',
            deckDescription: '',
            deckColour: 'black',
            deckFile: null
        }
    },
    methods: {
        ...mapActions({
            AddDeck: 'AddDeck'
        }),
        onSubmit() {
            if (!this.deckName) return

            this.AddDeck({
                'name': this.deckName,
                'description': this.deckDescription,
                'colour': this.deckColour
            })
        },
        uploadFile: (event) => {
            console.log('Uploading File ')
            let formData = new FormData()
            const fileo = event.target.files[0]
            formData.append('file', fileo)
            axios.post('http://localhost:5000/flashcards/import', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'token': document.cookie.split(';')[1]
                }
            })
                .then(res => console.log(res.data))
        }
    },
}

</script>

<style scoped = true>
div {
    opacity: 85%
}
</style>