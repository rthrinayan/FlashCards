<template>
    <div class="card" style="width: 30rem;" styl="justf">
        <div class="card-body">
            <div class="card-title">
                <div class="btn-group" role="group" aria-label="Basic example">
                    <button type="button" class="btn btn-outline-info" v-on:click="toggleSeen(false)">Sign In</button>
                    <button type="button" class="btn btn-outline-info" v-on:click="toggleSeen(true)">Sign Up</button>
                </div>
            </div>
            <h6 class="card-subtitle mb-2 text-muted" v-show="this.newUser">Make a new account to start your journey
            </h6>
            <h6 class="card-subtitle mb-2 text-muted" v-show="!this.newUser">Welcome back</h6>
            <p class="card-text">

            <div class="input-group mb-3">
                <input type="text" class="form-control" placeholder="Username" aria-label="Username"
                    v-model="this.username">
                <span class="input-group-text">@</span>

            </div>
            <div class="input-group mb-3" v-show="newUser">
                <span class="input-group-text">+91</span>
                <input type="text" class="form-control" aria-label="Phone Number" v-model="this.phoneNumber">
            </div>

            <div class="input-group mb-3" v-show="newUser">
                <input type="text" class="form-control" placeholder="Your Gmail" aria-label="Recipient's username"
                    aria-describedby="basic-addon2" v-model="this.email">
                <span class="input-group-text" id="basic-addon2">@gmail.com</span>
            </div>

            <div class="input-group mb-3" v-show="newUser">
                <div class="form-group">
                    <input type="password" class="form-control" id="password" placeholder="Password"
                        v-model="this.password">
                </div>
                <div class="form-group">
                    <input type="password" class="form-control" id="confimpasword" placeholder="Confirm"
                        v-model="this.confirmPassword">
                </div>
            </div>
            <input type="password" class="form-control " id="login" placeholder="Enter password" v-model="password"
                v-show="!newUser" />
            <button class="btn btn-outline-success" type="button" v-on:click="onSubmit"> Continue </button>

            </p>
        </div>
        <div class="alert alert-warning" role="alert" v-show="this.$store.state.loginError">
            {{this.$store.state.login_error}}
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex'
import { mapMutations } from 'vuex'
export default {
    name: 'LoginView',
    data() {
        return {
            newUser: false,
            username: '',
            phoneNumber: '',
            email: '',
            password: '',
            confirmPassword: '',

        }
    },
    methods: {
        ...mapActions({
            signIn: 'signIn',
            signUp: 'signUp'
        }),
        ...mapMutations({
            updateDetails: 'updateUserDetails',
            changeError: 'updateError'
        }),
        toggleSeen(val) {
            this.newUser = val
        },
        onSubmit() {
            if (this.newUser) {
                if (this.password === this.confirmPassword && this.email && this.phoneNumber && this.username) {
                    let userObj = {
                        'username': this.username,
                        'phone_number': this.phoneNumber,
                        'email': this.email,
                        'password': this.password
                    }
                    console.log(userObj)
                    this.signUp(userObj)
                }
                else {
                    error = 'Please fill the fields properly'
                    this.changeError(error)
                }
            } else {
                let userObj = {
                    'username': this.username,
                    'password': this.password
                }
                this.signIn(userObj)
            }
        }
    },

}
</script>

<style>
button {
    margin-top: 1em;
    margin-bottom: 1em;
}
</style>