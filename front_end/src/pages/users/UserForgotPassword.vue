<template>
  <div class="login-form">
    <h2 class="heading-secondary ma-bt-lg">Password Reset</h2>
    <form @click.prevent="requestReset" class="form__group">
      <div class="form__group ma-bt-md">
        <label for="password" class="form__label">Email</label>
        <input
          type="email"
          placeholder="your_email@email.com"
          id="email"
          class="form__input"
          v-model="email"
        />
      </div>

      <div class="form__group">
        <button class="btn btn--green">Request Reset Password</button>
      </div>
    </form>
    <div
      v-if="flashMessage"
      class="alert"
      :class="{ 'alert-success': isSuccess, 'alert-danger': isError }"
    >
      {{ successMessage }}
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      isValid: true,
      successMessage: "",
      flashMessage: false,
      isSuccess: false,
      isError: false,
    };
  },
  methods: {
    async requestReset() {
      this.isValid = true;
      if (this.email == "" || !this.email.includes("@")) {
        this.isValid = false;
        return;
      }

      const body = { email: this.email };

      try {
        const response = await axios({
          method: "post",
          url: `http://127.0.0.1:8000/api/v1/users/forgotpassword`,
          data: body,
        });
        if (response.status == 200) {
          this.successMessage = response.data.message;
          this.flashMessage = true;
          this.isSuccess = true;
        }
      } catch (err) {
        this.successMessage = err.response.data.detail;
        this.flashMessage = true;
        this.isError = true;
      }
    },
  },
};
</script>
