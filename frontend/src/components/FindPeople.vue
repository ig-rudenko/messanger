<script setup lang="ts">
import { ref } from "vue";

const visible = ref(false);
const search = ref("");
</script>

<template>
<div>
<!--  <Button icon="pi pi-search" @click="visible=!visible"/>-->
  <input class="rounded-2xl px-3 py-1 text-sm w-full bg-transparent active:border-0 focus:border-0 focus:outline-none"
    v-model="search" placeholder="Поиск людей"/>
</div>

  <Dialog v-model:visible="visible" modal header="Edit Profile" pt:root:class="!border-0 !bg-transparent" pt:mask:class="backdrop-blur-sm">
    <span class="text-surface-500 dark:text-surface-400 block mb-8">Update your information.</span>
    <div class="flex items-center gap-4 mb-4">
      <label for="username" class="font-semibold w-24">Username</label>
      <InputText id="username" class="flex-auto" autocomplete="off" />
    </div>
    <div class="flex items-center gap-4 mb-8">
      <label for="email" class="font-semibold w-24">Email</label>
      <InputText id="email" class="flex-auto" autocomplete="off" />
    </div>
    <div class="flex justify-end gap-2">
      <Button type="button" label="Cancel" severity="secondary" @click="visible = false"></Button>
      <Button type="button" label="Save" @click="visible = false"></Button>
    </div>
  </Dialog>

</template>

<style scoped>

</style>