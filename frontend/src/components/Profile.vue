<script setup lang="ts">

import {Ref, ref} from "vue";
import {getCurrentTheme, setAutoTheme, setDarkTheme, setLightTheme, ThemesValues} from "@/services/themes";
import {useStore} from "vuex";
import {User} from "@/services/user.ts";
import {getAvatar} from "@/services/formats.ts";

defineProps({
  isConnected: {
    required: false,
    type: Boolean,
    default: true,
  }
})
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
  location.href = "/auth/login";
}

</script>

<template>
  <div v-if="user"
      class="p-3 border-b-2 dark:border-gray-900 flex flex-wrap justify-between items-center gap-4 bg-gray-300 dark:bg-gray-700">
    <div class="flex flex-wrap items-center gap-4">
      <Avatar :image="getAvatar(user.username, '', 128)"
              class="mr-2" size="xlarge" shape="circle"/>
      <div>
        <div class="py-1 text-xl font-semibold">{{ user.firstName }} {{ user.lastName }}</div>
        <div class="text-sm font-mono">
          <span class='text-xs text-surface-500 dark:text-surface-400 font-mono pr-1'>id:</span>
          <span class="select-all cursor-pointer">{{user.username}}</span>
        </div>
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

    <div v-if="!isConnected" class="w-full inline-flex items-center px-4 font-semibold text-sm transition select-none">
      <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Подключение...
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