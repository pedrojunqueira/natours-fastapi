<template>
  <main class="main">
    <div class="card-container">
      <tour-card
        v-for="tour in allTours"
        :key="tour.id"
        :tourId="tour.id"
        :name="tour.name"
        :duration="tour.duration"
        :maxGroupSize="tour.maxGroupSize"
        :location="tour.startLocation.description"
        :description="tour.description"
        :rating="tour.ratingsAverage"
        :price="tour.price"
        :summary="tour.summary"
        :stops="tour.locations.length"
        :image="tour.imageCover"
      >
      </tour-card>
    </div>
  </main>
</template>

<script>
import TourCard from "../../components/tours/TourCard.vue";

export default {
  components: { TourCard },
  computed: {
    allTours() {
      return this.$store.getters.tours;
    },
  },
  created() {
    this.loadTours();
  },
  methods: {
    async loadTours() {
      await this.$store.dispatch("loadTours");
    },
  },
};
</script>
