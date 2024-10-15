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
  <div class="p-3 border-b-2 flex gap-4 hover:bg-gray-100 cursor-pointer">
    <div class="flex items-baseline relative">
      <Avatar class="p-overlay-badge" :image="chat.image" shape="circle" size="large" />
      <div v-if="chat.online" class="absolute p-[0.4rem] bg-green-500 rounded-full border-white border-2 -right-1 -bottom-1"></div>
    </div>
    <div class="w-full">
      <div class="flex justify-between">
        <span class="font-semibold">{{ chat.name }}</span>
        <span>{{ chat.lastDatetime }}</span>
      </div>
      <div class="text-gray-500">{{ chat.lastMessage }}</div>
    </div>
  </div>
</template>

<style scoped>

</style>