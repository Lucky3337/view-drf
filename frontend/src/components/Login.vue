<template>
	<div class="container">
		<div class="row">
			<div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
				<div class="card card-signin my-5">
					<div class="card-body">
						<h5 class="card-title text-center">Sign In</h5>
						<div class="form-label-group">
							<input v-model="login" type="text" id="inputEmail" class="form-control"
								   placeholder="Username" required autofocus>
							<label for="inputEmail">username</label>
						</div>

						<div class="form-label-group">
							<input v-model="password" type="password" id="inputPassword" class="form-control"
								   placeholder="Password" required>
							<label for="inputPassword">password</label>
						</div>
						<div class="row">
							<div class="col-sm-6">
								<button @click="registration" type="button" class="btn btn-outline-dark btn-block text-uppercase">
									Registration
								</button>
							</div>
							<div class="col-sm-6">
								<button @click="setLogin" class="btn btn-md btn-primary btn-block text-uppercase">Sign in</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
    import $ from 'jquery'
	import Registration from '@/components/Registration'

    export default {
        name: "Login",
        data() {
            return {
                login: '',
                password: '',
            }
        },
		components: {
            Registration,
        },
        methods: {
            setLogin() {
                $.ajax({
                    url: 'http://localhost:8000/authentication/token/',
                    type: 'POST',
                    data: {
                        username: this.login,
                        password: this.password
                    },
                    success: (response) => {
                        console.log(response.access_token);
                        localStorage.setItem("access_token", response.access_token);
                        localStorage.setItem("refresh_token", response.refresh_token);
                        localStorage.setItem("username", this.login);
                        if (localStorage.getItem("access_token")) {
                            window.location = '/';
                        }

                    },
                    error: (response) => {
                        console.log(response)
                        alert("Login or password isn't correct!");
                    }
                })
            },
			registration(){
                this.$router.push({
                    name: 'registration'
                })
			}
        }
    }
</script>

<style scoped>

</style>
