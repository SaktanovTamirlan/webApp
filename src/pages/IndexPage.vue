<template>
  <div>
    <q-btn @click="showToken" label="Show Token" />
  </div>
</template>

<script setup>
const showToken = () => {
  const cookies = document.cookie.split(";").map((cookie) => cookie.trim());
  const accessTokenCookie = cookies.find((cookie) =>
    cookie.startsWith("access_token=")
  );

  if (accessTokenCookie) {
    const accessToken = accessTokenCookie.split("=")[1];
    console.log("Access Token:", accessToken);
  } else {
    console.log("Access Token не найден в cookie");
  }
};
</script>
