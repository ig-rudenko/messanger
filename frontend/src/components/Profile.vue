<script setup lang="ts">

import {Ref, ref} from "vue";
import {getCurrentTheme, setAutoTheme, setDarkTheme, setLightTheme, ThemesValues} from "@/services/themes";
import {useStore} from "vuex";
import {User} from "@/services/user.ts";
import router from "@/router.ts";

const currentTheme: Ref<ThemesValues> = ref(getCurrentTheme())

const toggle = () => {
  if (currentTheme.value == "auto") setLightTheme();
  if (currentTheme.value == "light") setDarkTheme();
  if (currentTheme.value == "dark") setAutoTheme();
  currentTheme.value = getCurrentTheme();
}

const store = useStore()
const user: User|null = store.state.auth.user


function logout() {
  store.dispatch("auth/logout");
  router.push("/auth/login");
}

</script>

<template>
  <div v-if="user"
      class="p-3 border-b-2 dark:border-gray-900 flex flex-wrap justify-between items-center gap-4 bg-gray-300 dark:bg-gray-700">
    <div class="flex flex-wrap items-center gap-4">
      <Avatar image="https://primefaces.org/cdn/primevue/images/organization/walter.jpg" class="mr-2" size="xlarge"
              shape="circle"/>
      <div>
        <div class="text-xl font-semibold">{{ user.firstName }} {{ user.lastName }}</div>
      </div>
    </div>
    <div>

      <Button icon="pi pi-circle" v-if="currentTheme == 'auto'" @click="toggle" v-tooltip.bottom="'Влючить светлую тему'"
              class="hover:text-gray-900 dark:text-gray-400 hover:dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 bg-opacity-15"
              text/>
      <Button icon="pi pi-sun" v-if="currentTheme == 'light'" @click="toggle" v-tooltip.bottom="'Влючить темную тему'"
              class="hover:text-gray-900 dark:text-gray-400 hover:dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 bg-opacity-15"
              text/>
      <Button icon="pi pi-moon" v-if="currentTheme == 'dark'" @click="toggle" v-tooltip.bottom="'Выбрать тему автоматически'"
              class="hover:text-gray-900 dark:text-gray-400 hover:dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 bg-opacity-15"
              text/>

      <Button icon="pi pi-cog"
              class="hover:text-gray-900 dark:text-gray-400 hover:dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 bg-opacity-15"
              text/>
      <Button v-tooltip.bottom="'Выйти'" icon="pi pi-sign-out" @click="logout"
              class="dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-100 dark:hover:bg-gray-600 bg-opacity-10"
              text/>
    </div>
  </div>

</template>

<style scoped>

</style>