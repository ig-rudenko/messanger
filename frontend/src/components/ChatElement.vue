<script setup lang="ts">

import {ChatElementType} from "@/services/chats";
import {PropType} from "vue";

defineProps({
  chat: {
    required: true,
    type: Object as PropType<ChatElementType>
  }
})
</script>

<template>
  <div class="p-3 dark:bg-gray-700 dark:border-gray-900 border-b-2 flex gap-4 hover:bg-gray-200 dark:hover:bg-gray-900 cursor-pointer">
    <div class="flex items-baseline relative">
      <Avatar class="p-overlay-badge" :image="chat.image" shape="circle" size="large" />
      <div v-if="chat.online">
        <div class="absolute p-[0.4rem] bg-green-500 rounded-full border-2 dark:border-gray-600 animate-ping -right-1 -bottom-1"></div>
        <div class="absolute p-[0.4rem] bg-green-500 rounded-full border-2 dark:border-gray-600 border-opacity-5 -right-1 -bottom-1"></div>
      </div>
    </div>
    <div class="w-full">
      <div class="flex justify-between">
        <span class="font-semibold">{{ chat.name }}</span>
        <span>{{ chat.lastDatetime }}</span>
      </div>
      <div class="text-gray-500 dark:text-gray-400">{{ chat.lastMessage }}</div>
    </div>
  </div>
</template>

<style scoped>

</style>