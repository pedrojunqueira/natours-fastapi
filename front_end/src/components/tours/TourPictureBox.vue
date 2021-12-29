<template>
  <div class="picture-box">
    <img
      class="picture-box__img picture-box__img--1"
      :src="tourImage"
      alt="The Park Camper Tour 1"
    />
  </div>
</template>

<script>
export default {
  props: ["image"],
  computed: {
    tourImage() {
      return require(`@/assets/img/tours/${this.image}`);
    },
  },
};
</script>
