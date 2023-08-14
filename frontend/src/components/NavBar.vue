<template>
    <nav class="navbar navbar-expand-lg bg-light">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/">
                <img src="/docs/5.2/assets/brand/bootstrap-logo.svg" alt="" width="30" height="24"
                    class="d-inline-block align-text-top">
                Flask-Hearts
            </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link class="nav-link active" aria-current="page" to="/dashboard">Dashboard</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/flashcards">FlashCards</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/notes">Notes</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link  " to="/quizzes">Quizzes</router-link>
                    </li>

                </ul>

            </div>
            <div>
                <span class="navbar-text" style="justify-content:center;" v-show="!this.authenticated">
                    <router-link class="nav-link " to="/login">Login</router-link>
                </span>
                <span class="navbar-text" style="justify-content:center;" v-show="this.authenticated">
                    <router-link class="nav-link " to="/">Exit </router-link>
                </span>
            </div>
        </div>
    </nav>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'NavBar',
    computed: {
        ...mapState(['authenticated', 'name', 'rep', 'number', 'email', 'error'])
    }
}
</script>

<style>
li {
    padding-left: 1em;
}

span {
    padding-right: 10em;
}
</style>
