<template>
  <div class="overview-box__detail">
    <img :src="guideImage" alt="Lead guide" class="overview-box__img" />
    <!-- <img src="" alt="Lead guide" class="overview-box__img" /> -->
    <span class="overview-box__label">{{ guide.role }}</span>
    <span class="overview-box__text">{{ guide.name }}</span>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      guide: {},
    };
  },
  props: ["tourGuide"],
  methods: {
    async fetchGuide() {
      try {
        const headers = {
          Authorization: `Bearer ${this.$store.getters.token}`,
        };
        const response = await axios({
          method: "get",
          url: `http://127.0.0.1:8000/api/v1/users/${this.tourGuide}`,
          headers,
        });
        if (response.status == 200) {
          this.guide = response.data.user;
        }
      } catch (err) {
        console.log(err.response);
      }
    },
  },
  computed: {
    guideImage() {
      const photo = this.guide.photo;
      return photo
        ? require(`@/assets/img/users/${photo}`)
        : require(`@/assets/img/users/default.jpg`);
    },
  },
  created() {
    this.fetchGuide();
  },
};
</script>
