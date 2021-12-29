<template>
  <svg
    class="reviews__star"
    :class="{
      'reviews__star--active': isActive,
      'reviews__star--inactive': isInactive,
    }"
  >
    <use xlink:href="../../assets/img/icons.svg#icon-star"></use>
  </svg>
</template>

<script>
export default {
  props: ["status"],
  data() {
    return {
      isActive: true,
      isInactive: false,
    };
  },
  created() {
    if (this.status == "inactive") {
      this.isActive = false;
      this.isInactive = true;
    }
  },
};
</script>
