<template>
  <div v-if="selectedTour">
    <section class="section-header">
      <div class="heading-box">
        <h1 class="heading-primary">
          <span>{{ selectedTour.name }}</span>
        </h1>
        <div class="heading-box__group">
          <div class="heading-box__detail">
            <svg class="heading-box__icon">
              <use xlink:href="img/icons.svg#icon-clock"></use>
            </svg>
            <span class="heading-box__text"
              >{{ selectedTour.duration }} days</span
            >
          </div>
          <div class="heading-box__detail">
            <svg class="heading-box__icon">
              <use xlink:href="img/icons.svg#icon-map-pin"></use>
            </svg>
            <span class="heading-box__text">
              {{ selectedTour.startLocation.description }}</span
            >
          </div>
        </div>
      </div>
    </section>

    <section class="section-description">
      <div class="overview-box">
        <div>
          <div class="overview-box__group">
            <h2 class="heading-secondary ma-bt-lg">Quick facts</h2>
            <div class="overview-box__detail">
              <svg class="overview-box__icon">
                <use xlink:href="img/icons.svg#icon-calendar"></use>
              </svg>
              <span class="overview-box__label">Next date </span>
              <span class="overview-box__text"> {{ nextDate }} </span>
            </div>
            <div class="overview-box__detail">
              <svg class="overview-box__icon">
                <use xlink:href="img/icons.svg#icon-trending-up"></use>
              </svg>
              <span class="overview-box__label">Difficulty</span>
              <span class="overview-box__text">{{
                selectedTour.difficulty
              }}</span>
            </div>
            <div class="overview-box__detail">
              <svg class="overview-box__icon">
                <use xlink:href="img/icons.svg#icon-user"></use>
              </svg>
              <span class="overview-box__label">Participants</span>
              <span class="overview-box__text"
                >{{ selectedTour.maxGroupSize }} people</span
              >
            </div>
            <div class="overview-box__detail">
              <svg class="overview-box__icon">
                <use xlink:href="img/icons.svg#icon-star"></use>
              </svg>
              <span class="overview-box__label">Rating</span>
              <span class="overview-box__text"
                >{{ selectedTour.ratingsAverage }} / 5</span
              >
            </div>
          </div>

          <div class="overview-box__group">
            <h2 class="heading-secondary ma-bt-lg">Your tour guides</h2>
            <tour-guide
              v-for="guide in selectedTour.guides"
              :key="guide"
              :tourGuide="guide"
            ></tour-guide>
          </div>
        </div>
      </div>

      <div class="description-box">
        <h2 class="heading-secondary ma-bt-lg">About the park camper tour</h2>
        <p class="description__text">
          {{ selectedTour.description }}
        </p>
        <p class="description__text">
          {{ selectedTour.summary }}
        </p>
      </div>
    </section>

    <section class="section-pictures">
      <tour-picture-box
        v-for="pic in selectedTour.images"
        :key="pic"
        :image="pic"
      ></tour-picture-box>
    </section>

    <section class="section-map">
      <div id="map">
        <!-- Script to include mapblox  -->
      </div>
    </section>

    <section class="section-reviews">
      <div class="reviews">
        <tour-review
          v-for="review in reviews"
          :key="review.id"
          :review="review"
        ></tour-review>
      </div>
    </section>

    <section class="section-cta">
      <div class="cta">
        <div class="cta__img cta__img--logo">
          <img
            src="../../assets/img/logo-white.png"
            alt="Natours logo"
            class=""
          />
        </div>
        <img
          src="../../assets/img/tours/tour-5-2.jpg"
          alt=""
          class="cta__img cta__img--1"
        />
        <img
          src="../../assets/img/tours/tour-5-1.jpg"
          alt=""
          class="cta__img cta__img--2"
        />

        <div class="cta__content">
          <h2 class="heading-secondary">Liked this tour?</h2>
          <p class="cta__text">Your feedback is very important for us!</p>

          <router-link class="btn btn--green span-all-rows" :to="reviewTourLink"
            >Review this tour now!</router-link
          >
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import TourPictureBox from "./TourPictureBox.vue";
import TourGuide from "./TourGuide.vue";
import TourReview from "./TourReview.vue";
import axios from "axios";

export default {
  components: { TourPictureBox, TourGuide, TourReview },
  props: ["selectedTour"],
  data() {
    return {
      reviews: [],
    };
  },
  computed: {
    nextDate() {
      const startDates = this.selectedTour.startDates;
      const nextStart = new Date(startDates[0]);
      const month = nextStart.toLocaleString("default", { month: "long" });
      const year = nextStart.getFullYear();
      return `${month}  ${year}`;
    },
    reviewTourLink() {
      return `/tour_review/${this.$route.params.id}`;
    },
  },
  created() {
    this.fetchReviews();
  },
  methods: {
    async fetchReviews() {
      try {
        const headers = {
          Authorization: `Bearer ${this.$store.getters.token}`,
        };
        const response = await axios({
          method: "get",
          url: `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/tours/${this.$route.params.id}/reviews`,
          headers,
        });
        if (response.status == 200) {
          this.reviews = response.data.data.reviews;
        }
      } catch (err) {
        console.log(err.response);
      }
    },
  },
};
</script>
