<template>
  <div class="login-form">
    <h2 class="heading-secondary ma-bt-lg">Log into your account</h2>
    <form @click.prevent="resetPassword" class="form__group">
      <div class="form__group ma-bt-md">
        <label for="password" class="form__label">New Password</label>
        <input
          type="password"
          placeholder="*********"
          id="password"
          class="form__input"
          v-model="password"
        />
      </div>
      <div class="form__group ma-bt-md">
        <label for="confirm_password" class="form__label"
          >Confirm New Password</label
        >
        <input
          type="password"
          placeholder="*********"
          id="confirm_password"
          class="form__input"
          v-model="confirm_password"
        />
      </div>
      <p v-if="passwordMismatch">password do not match</p>
      <div class="form__group">
        <button class="btn btn--green">Reset Password</button>
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
      password: "",
      confirm_password: "",
      isValid: true,
      successMessage: "",
      flashMessage: false,
      isSuccess: false,
      isError: false,
    };
  },
  computed: {
    passwordMismatch() {
      return (
        this.password != this.confirm_password &&
        this.confirm_password.length > 3
      );
    },
  },
  methods: {
    async resetPassword() {
      this.isValid = true;
      if (this.password.length < 4 || this.confirm_password.length < 4) {
        this.isValid = false;
        return;
      }

      const body = {
        password: this.password,
        confirm_password: this.confirm_password,
      };
      const token = this.$route.params.reset_token;
      const url = `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/users/resetpassword/${token}`;

      try {
        const response = await axios({
          method: "patch",
          url,
          data: body,
        });
        if (response.status == 200) {
          this.successMessage = response.data.message;
          this.flashMessage = true;
          this.isError = false;
          this.isSuccess = true;
        }
      } catch (err) {
        this.successMessage = err.response.data.detail;
        this.flashMessage = true;
        this.isSuccess = false;
        this.isError = true;
      }
    },
  },
};
</script>
