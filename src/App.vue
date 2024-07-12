<template>
  <div>
    <AppComponent :authorizedUserButton="authorizedUserButton" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import AppComponent from "./layouts/AppComponent.vue";
defineOptions({
  name: "App",
});

const authorizedUserButton = ref([
  {
    label: "Домой",
    link: "/",
    icon: "home",
  },
  {
    label: "Профиль",
    link: "/profile",
    icon: "group",
  },
]);
</script>
