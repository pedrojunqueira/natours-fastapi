<template>
  <div class="login-form">
    <h2 class="heading-secondary ma-bt-lg">Tour review</h2>
    <form @click.prevent="submitForm" class="form__group">
      <div class="form__group ma-bt-md">
        <label for="review" class="form__label">Write you review</label>
        <textarea
          name="review"
          cols="40"
          rows="5"
          class="form__input"
          id="review"
          v-model="review"
        ></textarea>
      </div>
      <div class="form__group ma-bt-md">
        <label for="rating" class="form__label">rating</label>
        <select name="rating" id="rating" class="form__input" v-model="rating">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5" selected>5</option>
        </select>
        <!-- <input type="text" id="rating" class="form__input" v-model="rating" /> -->
      </div>
      <div class="form__group">
        <button class="btn btn--green">Submit your review</button>
      </div>
    </form>
    <div
      v-if="flashMessage"
      class="alert"
      :class="{ 'alert-success': isSuccess, 'alert-danger': isError }"
    >
      {{ message }}
    </div>
    <p v-if="!isValid">please review must not be empty</p>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      review: "",
      rating: "",
      isValid: true,
      error: null,
      message: "",
      flashMessage: false,
      isSuccess: false,
      isError: false,
    };
  },
  methods: {
    async submitForm() {
      this.isValid = true;
      if (this.review == "" || this.rating.length == 0) {
        this.isValid = false;
        return;
      }
      const payload = { review: this.review, rating: +this.rating };
      try {
        const headers = {
          Authorization: `Bearer ${this.$store.getters.token}`,
        };
        const response = await axios({
          method: "post",
          url: `http://127.0.0.1:8000/api/v1/tours/${this.$route.params.id}/reviews`,
          data: payload,
          headers,
        });
        if (response.status == 200) {
          console.log(response);
          this.message = "Thanks for submitting a review";
          this.flashMessage = true;
          this.isSuccess = true;
        }
      } catch (err) {
        this.message = err.response.data.detail;
        this.flashMessage = true;
        this.isError = true;
      }
    },
  },
};
</script>
