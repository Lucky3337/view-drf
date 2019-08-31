<template>
	<div class="row">
		<table class="table">
			<thead class="thead-dark">
			<tr>
				<th>#</th>
				<th>Nickname</th>
				<th>Breed</th>
				<th>Age</th>
				<th>Mass</th>
				<th>Hair</th>
				<th>Created</th>
			</tr>
			</thead>
			<tbody>
			<tr v-for="(cat1, index) in cats" v-bind:key="cat1.pk" @click="openModal(cat1)">
				<th scope="row">{{index+1}}</th>
				<td>{{cat1.nickname}}</td>
				<td>{{cat1.breed}}</td>
				<td>{{cat1.age}}</td>
				<td>{{cat1.mass}}</td>
				<td>{{cat1.hair}}</td>
				<td>{{cat1.created}}</td>
			</tr>
			</tbody>
		</table>
		<Modal v-if="show" :cat="cat"  @onChangeCat="onChangeCat" @closedModal="closedModal"></Modal>
	</div>
</template>

<script>
    import $ from 'jquery'
    import Modal from '@/components/cats/Modal'

    export default {
        name: "Cat",
        components: {
            Modal
        },
        data() {
            return {
                cats: Object,
                cat: {
                    pk: '',
                    nickname: '',
                    breed: '',
                    age: '',
                    mass: '',
                    hair: '',
                },
                show: false,
            }
        },
        created() {
            $.ajaxSetup({
                headers: {'Authorization': 'Bearer ' + localStorage.getItem("access_token")},
            });
            this.loadCats();
        },
        methods: {
            loadCats() {
                $.ajax({
                    url: 'http://84.201.170.191:8000/api/v1/cats/',
                    type: 'GET',
                    success: (response) => {
                        console.log(response);
                        this.cats = response.results;
                    },
                    error: (response) => {
                        console.log(response);
                        $.ajax({
                            url: 'http://84.201.170.191:8000/authentication/token/refresh/',
                            type: 'POST',
                            data: {
                                refresh_token: localStorage.getItem("refresh_token"),
                            },
                            success: (response) => {
                                localStorage.setItem("access_token", response.access_token);
                                localStorage.setItem("refresh_token", response.refresh_token);
                                this.loadCats();
                            }
                        })
                    }
                })
            },
            openModal(cat) {
                this.cat.pk = cat.pk;
                this.cat.nickname = cat.nickname;
                this.cat.breed = cat.breed;
                this.cat.age = cat.age;
                this.cat.mass = cat.mass;
                this.cat.hair = cat.hair;
                this.show = true;
                this.$bvModal.show('modal-scoped');
            },
            onChangeCat(cat) {
                this.closedModal();
				this.loadCats();

            },
            closedModal(){
                this.show = false;
			}
        }
    }
</script>

<style scoped>

</style>
