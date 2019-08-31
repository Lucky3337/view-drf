<template>
	<div>
		<form>
			<div class="form-group row">
				<label for="input-add-nickname" class="col-sm-2 col-form-label">Nickname</label>
				<div class="col-sm-10">
					<input v-model="nickname" type="text" class="form-control" id="input-add-nickname" placeholder="A cat">
				</div>
			</div>
			<div class="form-group row">
				<label for="input-add-breed" class="col-sm-2 col-form-label">Breed</label>
				<div class="col-sm-10">
					<input v-model="breed" type="text" class="form-control" id="input-add-breed" placeholder="Scotland">
				</div>
			</div>
			<div class="form-group row">
				<label for="input-add-age" class="col-sm-2 col-form-label">Age</label>
				<div class="col-sm-10">
					<input  v-model="age" type="text" class="form-control" id="input-add-age" placeholder="Age">
				</div>
			</div>
			<div class="form-group row">
				<label for="input-add-mass" class="col-sm-2 col-form-label">Mass</label>
				<div class="col-sm-10">
					<input  v-model="mass" type="text" class="form-control" id="input-add-mass" placeholder="Mass">
				</div>
			</div>
			<div class="form-group row">
				<label for="input-add-hair" class="col-sm-2 col-form-label">Hair</label>
				<div class="col-sm-10">
					<select v-model="hair" id="input-add-hair" class="custom-select">
						<option id="long" value="long">Long</option>
						<option id="short" value="short">Short</option>
						<option id="semi-long" value="semi-long">Semi-long</option>
					</select>
				</div>
			</div>
			<div class="form-group row">
				<div class="col-sm-10 offset-sm-2">
					<button type="submit" class="btn btn-primary" @click="addCat">Add</button>
				</div>
			</div>
		</form>
	</div>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: "Add",
		data() {
            return{
                nickname: '',
				breed: '',
				age: '',
				mass: '',
				hair: '',
			}
		},
        created() {
            $.ajaxSetup({
                headers: {'Authorization': 'Bearer ' + localStorage.getItem("access_token")},
            });
        },
		methods: {
            addCat(){
            	$.ajax({
                    url: 'http://84.201.170.191:8000/api/v1/cats/',
                    type: 'POST',
                    data: {
                        'nickname': this.nickname,
                        'breed': this.breed,
                        'age': this.age,
                        'mass': this.mass,
                        'hair': this.hair,
                    },
                    success: (response) => {
                        console.log(response)
						window.location = '/'
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
		}
    }
</script>

<style scoped>

</style>
