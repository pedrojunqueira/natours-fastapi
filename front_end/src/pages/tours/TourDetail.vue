<template>
  <tour-item-detail :selectedTour="selectedTour"></tour-item-detail>
</template>

<script>
import axios from "axios";
import TourItemDetail from "../../components/tours/TourItemDetail.vue";

export default {
  components: { TourItemDetail },
  data() {
    return {
      selectedTour: null,
      tourId: null,
    };
  },
  created() {
    this.tourId = this.$route.params.id;
    this.loadTour(this.tourId);
  },
  methods: {
    async loadTour(Id) {
      //await this.$store.dispatch("loadTour", Id);
      const url = `http://127.0.0.1:8000/api/v1/tours/${Id}`;
      const response = await axios(url);
      if (response.status == 200) {
        const tour = response.data.data;
        this.selectedTour = tour;
      }
    },
  },
};
</script>
