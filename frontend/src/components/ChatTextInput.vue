<script setup lang="ts">
import {ref} from "vue";

const text = ref("")

const messageSendingIsBlocked = ref(false);
const blockMessageSending = () => messageSendingIsBlocked.value = true;
const unBlockMessageSending = () => messageSendingIsBlocked.value = false;

function sendMessage() {
  if (messageSendingIsBlocked.value) return;
  text.value = "";
}


</script>

<template>
<div class="flex items-center w-full p-2 border-t-1 border-indigo-200 dark:border-indigo-800 border-t-2">
  <Textarea v-model="text" class="w-full px-2 resize-none bg-opacity-0 border-0 focus:ring-0 focus:ring-surface-0 dark:focus:ring-gray-900" autofocus autoResize
            placeholder="Напишите своё сообщение"
            @keydown.shift.enter="blockMessageSending"
            @keyup.shift.enter="unBlockMessageSending"
            @keydown.enter="sendMessage" />
  <i class="pi pi-send w-10 h-10 p-3 text-2xl cursor-pointer" @click="sendMessage" />
</div>
</template>


<style scoped>
.border-t-1 {
  border-top-width: 1px;
}
.bg-opacity-0 {
  background-color: rgba(1,1,1,0);
}
</style>