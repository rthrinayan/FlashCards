<template>
    <div class="jumbotron">
        <h1 class="display-4">Hello, {{ usr.username }}!</h1>
        <p class="lead">This is the dashboard. Your activity is saved by us and analysed.</p>
        <hr class="my-4">
        <p>You will be able to view your statistics here</p>
        <br>
        <p> We will also mail them to you at : {{usr.email}}</p>

    </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
    name: 'DashView',
    data() {
        return {
            usr: null,
        }
    },
    computed: {
        ...mapGetters({
            getUser: 'getUserObj'
        })
    },
    created() {
        this.usr = this.getUser
    }
}
</script>