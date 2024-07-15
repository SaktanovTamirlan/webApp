<template>
  <div>
    <q-layout view="hHr LpR lFf" container style="height: 100vh">
      <q-header reveal elevated bordered style="background-color: transparent">
        <q-toolbar class="bg-white text-black">
          <q-btn flat round dense icon="menu" @click="drawer = !drawer" />
          <q-toolbar-title> Toolbar </q-toolbar-title>
        </q-toolbar>
      </q-header>
      <q-drawer
        v-model="drawer"
        :width="200"
        :breakpoint="500"
        content-class="bg-grey-3"
        bordered
      >
        <q-list bordered v-show="isAuthorized">
          <q-item clickable v-ripple @click="navigateLogin">
            <q-item-section avatar>
              <q-icon color="positive" name="login" />
            </q-item-section>
            <q-item-section>Войти в аккаунт</q-item-section>
          </q-item>
        </q-list>

        <q-list bordered v-show="isAuthorizedButton">
          <q-item
            clickable
            v-ripple
            v-for="button in authorizedUserButton"
            :key="button.label"
            @click="navigate(button.link)"
          >
            <q-item-section avatar>
              <q-icon :name="button.icon" />
            </q-item-section>
            <q-item-section>{{ button.label }}</q-item-section>
          </q-item>
        </q-list>
      </q-drawer>
      <q-page-container>
        <q-page padding>
          <router-view />
          <q-page-scroller
            position="bottom-right"
            :scroll-offset="150"
            :offset="[18, 18]"
          >
            <q-btn icon="keyboard_arrow_up" color="black" />
          </q-page-scroller>
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { onMounted, ref } from "vue";
import { useQuasar } from "quasar";
import axios from "axios";

const drawer = ref(false);
const isAuthorized = ref(true);
const isAuthorizedButton = ref(false);
const navigateLogin = () => {
  window.location.href = "http://localhost:8000/login";
};
const router = useRouter();
const $q = useQuasar();

const { props } = defineProps({
  authorizedUserButton: {
    type: Array,
    required: true,
  },
});

const checkAuthorizedUser = () => {
  isAuthorizedButton.value = ref(true);
  isAuthorized.value = false;
};

const navigate = (route) => {
  router.push(route);
};

onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:8000/user", {
      withCredentials: true,
    });
    const userInfo = response.data;
    console.log(userInfo);
    if (userInfo.name.length > 0) {
      checkAuthorizedUser();
    }
    localStorage.setItem("userName", userInfo.name);
    console.log(userInfo.realm_access);
  } catch (error) {
    console.error("Ошибка при получении Access Token:", error);
  }
});
</script>

<style scoped></style>
