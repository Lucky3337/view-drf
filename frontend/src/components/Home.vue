<template>
	<div>
		<div class="container">
			<nav class="navbar navbar-default">
				<div class="container-fluid">
					<div class="navbar-header">
						<!--						<a class="navbar-brand" href="#">Cats</a>-->
						<button v-if="auth" type="button" class="btn btn-primary" @click="addCatForm" id="btn-add-nc">
							{{btn_add_cat_form}}
						</button>
					</div>
					<ul class="nav navbar-nav navbar-right">
						<li>
							<div v-if="!auth">
								<button @click="login">Login</button>
							</div>
							<div v-else>
								<span>You're logging as: {{username}}</span>
								<button @click="logout">Logout</button>
							</div>
						</li>
					</ul>
				</div>
			</nav>
			<Add v-if="add_cat"></Add>
			<Cat v-else-if="auth"></Cat>
			<div v-else>You need to login or registration for using services</div>
		</div>
	</div>
</template>

<script>
    import $ from 'jquery'
    import Cat from "@/components/cats/Cat";
    import Add from "@/components/cats/Add";
    import Login from "./Login";

    export default {
        name: "Home",
        data() {
            return {
                username: localStorage.getItem("username"),
                add_cat: false,
                btn_add_cat_form: 'Add new cat',
            }
        },
        created() {
        },
        components: {
            Login,
            Cat,
            Add
        },
        computed: {
            auth() {
                if (localStorage.getItem("access_token")) {
                    return true;
                }
            }
        },
        methods: {
            login() {
                this.$router.push({
                    name: "login"
                })
            },
            logout() {
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                window.location = '/';
            },
            addCatForm() {
                if (this.add_cat) {
                    this.btn_add_cat_form = 'Add new cat';
                } else {
                    this.btn_add_cat_form = 'Wathching all cats';
                }
                this.add_cat = !this.add_cat;
            }
        }
    }
</script>

<style scoped>

</style>
