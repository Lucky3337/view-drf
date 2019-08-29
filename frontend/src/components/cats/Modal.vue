<template>
	<div>
		<b-modal no-close-on-backdrop no-close-on-esc id="modal-scoped">
			<template slot="modal-header">
				<!-- Emulate built in modal header close button action -->
				<b-button size="sm" variant="outline-danger" @click="close">
					Close Modal
				</b-button>
				<h5>Modification</h5>
			</template>

			<template slot="default" slot-scope="{ hide }">
				<div class="container">
					<div class="form-group row">
						<label class="col-sm-3 col-form-label" for="nickname">Nickname</label>
						<div class="col-sm-9">
							<input type="text" id="nickname" v-model="data.nickname">
						</div>
					</div>
					<div class="form-group row">
						<label class="col-sm-3 col-form-label" for="breed">Breed</label>
						<div class="col-sm-9">
							<input type="text" id="breed" v-model="data.breed">
						</div>
					</div>
					<div class="form-group row">
						<label class="col-sm-3 col-form-label" for="age">Age</label>
						<div class="col-sm-9">
							<input type="text" id="age" v-model="data.age">
						</div>
					</div>
					<div class="form-group row">
						<label class="col-sm-3 col-form-label" for="mass">Mass</label>
						<div class="col-sm-9">
							<input type="text" id="mass" v-model="data.mass">
						</div>
					</div>
					<div class="form-group row">
						<label class="col-sm-3 col-form-label">Hair</label>
						<div class="col-sm-9">
							<b-form-select id="hair"
										   v-model="data.hair"
										   :options="data.options"
							></b-form-select>
						</div>
					</div>
				</div>
			</template>

			<template slot="modal-footer" slot-scope="{ hide }">
				<b-button size="sm" variant="success" @click="saveCat">
					save
				</b-button>
				<b-button size="sm" variant="danger" @click="deleteCat">
					delete
				</b-button>
			</template>
		</b-modal>
	</div>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: "Modal",
        props: {
            cat: {
                type: Object
			},
        },
        data() {
            return {
                data: {
                    pk: this.cat.pk,
                    nickname: this.cat.nickname,
                    breed: this.cat.breed,
                    age: this.cat.age,
                    mass: this.cat.mass,
                    hair: this.cat.hair,
                    options: ["long", "short", "semi-long"]
                },
            }
        },
        // watch: {
        //     data: {
        //         handler: function (val, oldVal) {
        //             console.log('новое значение: %s, старое значение: %s', val, oldVal);
        //             this.$emit('onChangeCat', val);
        //         },
        //         deep: true
        //     },
        // },
        methods: {
            saveCat() {
                $.ajax({
                    url: 'http://localhost:8000/api/v1/cats/' + this.cat.pk + '/',
                    type: 'PUT',
                    data: {
                        'nickname': this.data.nickname,
                        'breed': this.data.breed,
                        'age': this.data.age,
                        'mass': this.data.mass,
                        'hair': this.data.hair,
                    },
                    success: (response) => {
                        this.$emit('onChangeCat', this.data);
                        this.close();
                    }
                })
            },
            deleteCat() {
                $.ajax({
                    url: 'http://localhost:8000/api/v1/cats/' + this.cat.pk + '/',
                    type: 'DELETE',
                    data: {
                        'nickname': this.data.nickname,
                        'breed': this.data.breed,
                        'age': this.data.age,
                        'mass': this.data.mass,
                        'hair': this.data.hair,
                    },
                    success: (response) => {
                        this.$emit('onChangeCat', this.data);
                        this.close();
                    }
                })
            },
            close() {
                this.$bvModal.hide('modal-scoped');
                this.$emit('closedModal');
            },
        }
    }
</script>

<style scoped>

</style>
