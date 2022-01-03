<template>
  <header class="header">
    <nav class="nav nav--tours">
      <a href="/tours" class="nav__el">All tours</a>
    </nav>
    <div class="header__logo">
      <img src="../../assets/img/logo-white.png" alt="Natours logo" />
    </div>
    <nav class="nav nav--user">
      <a v-if="isLoggdedIn" href="#" class="nav__el">My bookings</a>
      <a v-if="isLoggdedIn" href="/user/me" class="nav__el">
        <img :src="meImage" alt="User photo" class="nav__user-img" />
        <span>{{ name }}</span>
      </a>

      <a v-if="!isLoggdedIn" href="/tours/login" class="nav__el">Log in</a>
      <a v-if="!isLoggdedIn" href="/tours/sign_up" class="nav__el">Sign up</a>
      <a v-if="isLoggdedIn" @click="logout" class="nav__el">Log out</a>
    </nav>
  </header>
</template>

<script>
export default {
  computed: {
    isLoggdedIn() {
      return this.$store.getters.isAuthenticated;
    },
    name() {
      return this.$store.getters.me.name;
    },
    meImage() {
      const photo = this.$store.getters.me.photo;
      try {
        const folder_photo = require(`@/assets/img/users/${photo}`);
        return folder_photo;
      } catch (err) {
        console.log(err.message);
      }
      return require(`@/assets/img/users/default.jpg`);
    },
  },
  methods: {
    logout() {
      this.$store.dispatch("logout");
      this.$router.replace("/tours");
    },
  },
};
</script>
