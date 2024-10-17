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

const logoutVisible = ref(false);

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
        <div class="py-1 text-xl font-semibold">{{ user.firstName }} {{ user.lastName }}</div>
        <div class="text-sm font-mono">{{user.username}}</div>
      </div>
    </div>
    <div>

      <Button icon="pi pi-circle" v-if="currentTheme == 'auto'" @click="toggle" v-tooltip="'Влючить светлую тему'"
              class="hover:text-gray-900 dark:text-gray-400 hover:dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 bg-opacity-15"
              text/>
      <Button icon="pi pi-sun" v-if="currentTheme == 'light'" @click="toggle" v-tooltip="'Влючить темную тему'"
              class="hover:text-gray-900 dark:text-gray-400 hover:dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 bg-opacity-15"
              text/>
      <Button icon="pi pi-moon" v-if="currentTheme == 'dark'" @click="toggle" v-tooltip="'Выбрать тему автоматически'"
              class="hover:text-gray-900 dark:text-gray-400 hover:dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 bg-opacity-15"
              text/>

      <Button icon="pi pi-cog"
              class="hover:text-gray-900 dark:text-gray-400 hover:dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 bg-opacity-15"
              text/>
      <Button v-tooltip="'Выйти'" icon="pi pi-sign-out" @click="logoutVisible=true"
              class="dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-100 dark:hover:bg-gray-600 bg-opacity-10"
              text/>
    </div>
  </div>

  <Dialog v-model:visible="logoutVisible" modal
          pt:root:class="border-0 bg-surface-200 dark:bg-surface-800 rounded-xl p-2"
          pt:mask:class="backdrop-blur-sm">
    <template #container="{ closeCallback }">
      <div class="p-4 text-xl font-semibold text-surface-800 dark:text-surface-200">Вы уверены, что хотите выйти?</div>
      <div class="flex justify-end gap-2 p-2">
        <Button type="button" label="Нет" severity="secondary" autofocus @click="closeCallback"></Button>
        <Button type="button" label="Выйти" severity="danger" @click="logout"></Button>
      </div>
    </template>
  </Dialog>


</template>

<style scoped>

</style>