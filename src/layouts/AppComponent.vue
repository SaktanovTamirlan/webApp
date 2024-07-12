<template>
  <div>
    <q-layout view="hHr LpR lFf" container style="height: 100vh">
      <q-header
        v-model="header"
        reveal
        elevated
        bordered
        style="background-color: transparent"
      >
        <q-toolbar class="bg-white text-black">
          <q-btn flat round dense icon="assignment_ind" />
          <q-toolbar-title> Toolbar </q-toolbar-title>
          <q-btn
            class="bg-black q-mr-xs text-white"
            style="width: 75px"
            dense
            no-caps
            label="Login"
            @click="loginBtn"
          />
          <q-btn
            color="primary"
            no-caps
            label="Token"
            @click="showAccessToken"
          />
        </q-toolbar>
      </q-header>
      <q-page-container>
        <q-page padding>
          <router-view />
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import axios from "axios";

const loginBtn = () => {
  window.location.href = "http://localhost:8000/login";
};

const router = useRouter();

const showAccessToken = async () => {
  try {
    const response = await axios.get("http://localhost:8000/user", {
      withCredentials: true,
    });
    const userInfo = response.data;
    console.log(userInfo);
  } catch (error) {
    console.error("Ошибка при получении Access Token:", error);
  }
};
</script>

<style scoped>
/* Ваши стили */
</style>
