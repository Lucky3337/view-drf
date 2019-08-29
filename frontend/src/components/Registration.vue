<template>
	<div class="container">
		<h2>Registration</h2>
		<b-form @submit="onSubmit">
			<b-form-group
				id="input-group-0"
				label="Email address:"
				label-for="input-0"
			>
				<b-form-input
					:state="validation"
					id="input-0"
					v-model="login"
					type="text"
					required
					placeholder="Enter login"

				></b-form-input>
				<b-form-invalid-feedback :state="validation">
					Your login must be 3-25 characters long.
				</b-form-invalid-feedback>
				<b-form-valid-feedback :state="validation">

				</b-form-valid-feedback>
			</b-form-group>

			<b-form-group id="input-group-1" label="Your password:" label-for="input-1">
				<b-form-input
					id="input-1"
					v-model="pass1"
					type='password'
					required
					placeholder="Enter password"
				></b-form-input>
				<b-form-invalid-feedback :state="validationPassword">
					Your password must be 6-25 characters long.
				</b-form-invalid-feedback>
				<b-form-valid-feedback :state="validationPassword">

				</b-form-valid-feedback>
			</b-form-group>

			<b-form-group id="input-group-2" label="Your password confirm:" label-for="input-2">
				<b-form-input
					id="input-2"
					v-model="pass2"
					type="password"
					required
					placeholder="Enter password confirm"
				></b-form-input>
				<b-form-invalid-feedback :state="validationPasswordConfirm">
					Your password must be 6-25 characters long.
				</b-form-invalid-feedback>
				<b-form-valid-feedback :state="validationPasswordConfirm">
				</b-form-valid-feedback>
			</b-form-group>

			<b-button @click="createUser" v-if="pass_equals" type="submit" variant="primary">Submit</b-button>
<!--			<button @click="onSubmit1" v-if="pass_equals" type="submit" >Submit</button>-->
			<b-alert v-else show>Passwords don't equals</b-alert>
		</b-form>
	</div>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: "Registration",
        data() {
            return {
                login: '',
				pass1: '',
				pass2: '',
                pass_equals: false,
            }
        },
        methods: {
            onSubmit:(evt) => {
                evt.preventDefault();
            },
			createUser(){
                console.log('qu qu')
				console.log(this.login)
                $.ajax({
                    url: 'http://localhost:8000/api/v1/users/',
                    type: 'POST',
                    data: {
                        username: this.login,
                        password: this.pass1,
                    },
                    success: (response) => {
						this.$router.push({
							name: 'login'
						})
                    }
                })
			}
        },
        computed: {
            validation() {
                return this.login.length > 4 && this.login.length < 25
            },
            validationPassword() {
                return this.pass1.length > 6 && this.pass1.length < 25
            },
            validationPasswordConfirm() {
                return this.pass2.length > 6 && this.pass2.length < 25

            }
        },
        watch: {
            pass1: {
                handler: function (val, oldVal) {
                    if ((val === this.pass1) && (this.validationPassword === this.validationPasswordConfirm)) {
                        this.pass_equals = true
                    } else {
                        this.pass_equals = false
                    }
                },
                deep: true
            },
			pass2: {
                handler: function (val, oldVal) {
                    if ((val === this.pass1) && (this.validationPassword === this.validationPasswordConfirm)) {
                        this.pass_equals = true
                    } else {
                        this.pass_equals = false
                    }
                },
                deep: true
            },
        }
    }
</script>

<style scoped>

</style>
