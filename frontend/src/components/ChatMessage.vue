<script setup lang="ts">
import {PropType} from "vue";

import {ChatMessageType} from "@/services/chats";
import {textToHtml, verboseDatetime} from "@/services/formats";

defineProps({
  message: {
    required: true,
    type: Object as PropType<ChatMessageType>
  },
  mark: {
    required: false,
    type: String,
    default: ""
  }
})


</script>

<template>
  <div class="m-1 p-3 rounded w-fit max-w-xl message" :mark="mark" :data-created-at="message.createdAt">
    <div class="pb-2"><span v-html="textToHtml(message.message)"></span></div>
    <div class="text-sm font-light" >{{ verboseDatetime(message.createdAt) }}</div>
  </div>
</template>

<style scoped>
</style>