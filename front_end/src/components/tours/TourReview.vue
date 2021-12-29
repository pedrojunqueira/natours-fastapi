<template>
  <div class="reviews__card">
    <div class="reviews__avatar">
      <img :src="userImage" :alt="user.name" class="reviews__avatar-img" />
      <h6 class="reviews__user">{{ userName }}</h6>
    </div>
    <p class="reviews__text">
      {{ review.review }}
    </p>
    <div class="reviews__rating">
      <tour-review-rating
        v-for="star in stars"
        :key="star"
        :status="star"
      ></tour-review-rating>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TourReviewRating from "./TourReviewRating.vue";

export default {
  components: { TourReviewRating },
  props: ["review"],
  created() {
    this.fetchUser();
  },
  data() {
    return {
      user: {},
    };
  },
  methods: {
    async fetchUser() {
      try {
        const headers = {
          Authorization: `Bearer ${this.$store.getters.token}`,
        };
        const response = await axios({
          method: "get",
          url: `http://127.0.0.1:8000/api/v1/users/${this.review.user}`,
          headers,
        });
        if (response.status == 200) {
          this.user = response.data.user;
        }
      } catch (err) {
        console.log(err.response);
      }
    },
  },
  computed: {
    userImage() {
      const photo = this.user.photo;
      return photo
        ? require(`@/assets/img/users/${photo}`)
        : require(`@/assets/img/users/default.jpg`);
    },
    userName() {
      return this.user.name ? this.user.name : "anonymous";
    },
    stars() {
      const stars = this.review.rating;
      const active = stars;
      const inactive = 5 - active;
      const starRating = [];
      for (let i = 0; i < active; i++) {
        starRating.push("active");
      }
      for (let i = 0; i < inactive; i++) {
        starRating.push("inactive");
      }
      return starRating;
    },
  },
};
</script>
