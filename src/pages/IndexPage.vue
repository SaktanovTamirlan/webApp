<template>
  <div>
    <div v-for="n in 180" :key="n">
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Iusto autem sint
      quae, temporibus fugit sapiente asperiores laudantium vitae aliquam
      corporis corrupti amet praesentium aperiam, laboriosam labore earum atque
      provident non!
    </div>
  </div>
</template>

<script setup>
import { onBeforeMount } from "vue";
const name = localStorage.getItem("userName");
onBeforeMount(() => {
  console.log(name);
});
</script>
