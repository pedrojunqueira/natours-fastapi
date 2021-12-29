<template>
  <div class="login-form">
    <h2 class="heading-secondary ma-bt-lg">Sign up to Natours app</h2>
    <form @click.prevent="submitForm" class="form__group">
      <div class="form__group ma-bt-md">
        <label for="text" class="form__label">username</label>
        <input
          type="text"
          id="username"
          placeholder="your username"
          class="form__input"
          v-model="username"
        />
      </div>
      <div class="form__group ma-bt-md">
        <label for="email" class="form__label">Email address</label>
        <input
          type="email"
          id="email"
          placeholder="your@email.com"
          class="form__input"
          v-model="email"
        />
      </div>
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
      <div class="form__group ma-bt-md">
        <label for="confirm-password" class="form__label"
          >Confirm Password</label
        >
        <input
          type="password"
          placeholder="*********"
          id="confirm-password"
          class="form__input"
          v-model="confirm_password"
        />
        <p v-if="passwordMismatch">password do not match</p>
      </div>

      <div class="form__group">
        <button class="btn btn--green">Sign up</button>
      </div>
    </form>
    <p v-if="!isValid">please fill in all form fields</p>
    <div class="form__group">
      <p class="form__label">Already have an account?</p>
      <a href="/tours/login" class="btn btn--green">Log In</a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirm_password: "",
      isValid: true,
    };
  },
  methods: {
    async submitForm() {
      this.isValid = true;
      if (
        this.username == "" ||
        this.email == "" ||
        this.password.length < 4 ||
        this.confirm_password.length < 4
      ) {
        this.isValid = false;
        return;
      }

      try {
        const payload = {
          username: this.username,
          email: this.email,
          password: this.password,
          confirm_password: this.confirm_password,
        };
        await this.$store.dispatch("signUp", payload);
        this.$router.replace("/user/me");
      } catch (err) {
        console.log(err);
      }
    },
  },
  computed: {
    passwordMismatch() {
      return (
        this.password != this.confirm_password &&
        this.confirm_password.length > 3
      );
    },
  },
};
</script>
