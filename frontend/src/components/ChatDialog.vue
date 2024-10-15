<script setup lang="ts">
import {ChatMessageType, ChatService} from "@/services/chats";
import {ref, Ref} from "vue";
import ChatMessage from "@/components/ChatMessage.vue";

const props = defineProps({
  chatId: {
    required: true,
    type: String,
  }
})

const currentUser = "igor"


const chatService = new ChatService()
const chatMessages: Ref<ChatMessageType[]> = ref([])

chatService.getChatMessages(props.chatId).then(value => chatMessages.value = value)

function getMessageClasses(msg: ChatMessageType, index: number): string[] {
  let classes = []
  if (!chatMessages.value[index-1] || chatMessages.value[index-1].senderUsername != msg.senderUsername) {
    classes.push("rounded-t-2xl")
  }
  if (!chatMessages.value[index+1] || chatMessages.value[index+1].senderUsername != msg.senderUsername) {
    classes.push("rounded-b-2xl")
  }
  if (msg.senderUsername == currentUser) {
    classes.push(...["self-end", "bg-gray-200"])
  } else {
    classes.push("bg-indigo-200")
  }
  console.log(msg.message, classes)
  return classes
}

</script>

<template>
<div v-if="chatMessages" class="w-full h-full flex flex-col p-10 overflow-y-auto">
  <template v-for="(msg, index) in chatMessages">
    <ChatMessage :message="msg" :class="getMessageClasses(msg, index)" />
  </template>
  <template v-for="(msg, index) in chatMessages">
    <ChatMessage :message="msg" :class="getMessageClasses(msg, index)" />
  </template>
  <template v-for="(msg, index) in chatMessages">
    <ChatMessage :message="msg" :class="getMessageClasses(msg, index)" />
  </template>
</div>
</template>

<style scoped>

</style>