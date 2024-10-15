<script setup lang="ts">
import {PropType} from "vue";
import {ChatMessageType} from "@/services/chats.ts";

defineProps({
  message: {
    required: true,
    type: Object as PropType<ChatMessageType>
  }
})

function verboseDatetime(timestamp: number): string {
  // multiplied by 1000 so that the argument is in milliseconds, not seconds
  const milliseconds = new Date(timestamp * 1000);
  const dateObject = new Date(milliseconds)
  return dateObject.toLocaleString("ru-RU")
}
</script>

<template>
  <div class="m-1 p-3 rounded w-fit">
    <div>{{ message.message }}</div>
    <div class="text-sm ">{{ verboseDatetime(message.timestamp) }}</div>
  </div>
</template>

<style scoped>

</style>