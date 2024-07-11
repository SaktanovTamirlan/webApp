<template>
  <div>
    <button @click="redirectToFastAPI">Click</button>
  </div>
</template>

<script>
export default {
  methods: {
    redirectToFastAPI() {
      window.location.href = "http://localhost:8000/login";
    },
  },
};
</script>

<style scoped>
/* Ваши стили */
</style>
