<template>
  <div class="login-form">
    <h2 class="heading-secondary ma-bt-lg">Log into your account</h2>
    <form @click.prevent="submitForm" class="form__group">
      <div class="form__group ma-bt-md">
        <label for="username" class="form__label">Username</label>
        <input
          type="text"
          id="username"
          placeholder="username"
          class="form__input"
          v-model="username"
        />
      </div>
      <router-link class="right" to="/forgot_password"
        >Forgot Password?</router-link
      >
      <!-- <a class="right" href="/tours/sign_up">Forgot Password?</a> -->
      <div class="form__group ma-bt-md">
        <label for="password" class="form__label">Password</label>
        <input
          type="password"
          placeholder="*********"
          id="password"
          class="form__input"
          v-model="password"
        />
      </div>
      <div class="form__group">
        <button class="btn btn--green">Login</button>
      </div>
    </form>
    <div class="form__group">
      <p class="form__label">Do not have an account?</p>
      <a href="/tours/sign_up" class="btn btn--green"> sign_up</a>
    </div>

    <div
      v-if="flashMessage"
      class="alert"
      :class="{ 'alert-success': isSuccess, 'alert-danger': isError }"
    >
      {{ message }}
    </div>
    <p v-if="!isValid">Please enter an username and password to Login</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
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
      if (this.username == "" || this.password < 4) {
        this.isValid = false;
        return;
      }
      const payload = { username: this.username, password: this.password };
      const response = await this.$store.dispatch("login", payload);
      if (response) {
        this.$router.replace("/user/me");
      } else {
        this.message = "username or password is incorrect";
        this.flashMessage = true;
        this.isSuccess = false;
        this.isError = true;
      }
    },
  },
};
</script>

<style scoped>
.right {
  float: right;
}
</style>
