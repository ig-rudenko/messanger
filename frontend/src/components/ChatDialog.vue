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

function scrollToEnd() {
  // Автопрокрутка к нижнему сообщению при открытии
  const container = document.getElementById('messages-container')!;
  container.scrollTop = container.scrollHeight;
}

chatService.getChatMessages(props.chatId).then(value => {
  chatMessages.value = value;
  setTimeout(scrollToEnd, 200)
})

function getMessageClasses(msg: ChatMessageType, index: number): string[] {
  let classes = []
  if (!chatMessages.value[index - 1] || chatMessages.value[index - 1].senderUsername != msg.senderUsername) {
    classes.push("rounded-t-2xl")
  }
  if (!chatMessages.value[index + 1] || chatMessages.value[index + 1].senderUsername != msg.senderUsername) {
    classes.push("rounded-b-2xl")
  }
  if (msg.senderUsername == currentUser) {
    classes.push(...["self-end", "bg-gray-200", "dark:bg-gray-700"])
  } else {
    classes.push(...["bg-indigo-200", "dark:bg-indigo-900"])
  }
  return classes
}

</script>

<template>
  <div v-if="chatMessages" id="messages-container" class="group w-full h-full flex flex-col p-10 overflow-y-auto">
    <template v-for="(msg, index) in chatMessages">
      <ChatMessage :message="msg" :class="getMessageClasses(msg, index)"/>
    </template>
    <template v-for="(msg, index) in chatMessages">
      <ChatMessage :message="msg" :class="getMessageClasses(msg, index)"/>
    </template>
    <template v-for="(msg, index) in chatMessages">
      <ChatMessage :message="msg" :class="getMessageClasses(msg, index)"/>
    </template>
  </div>
</template>

<style scoped>
::-webkit-scrollbar {
  display: inline;
  width: 7px;
  height: 5px;
}
::-webkit-scrollbar-track-piece {
  background-color: var(--p-surface-900);
  border-radius: 20px;
  opacity: 0.2;
}
.group:hover::-webkit-scrollbar-track-piece {
  background-color: var(--p-surface-600);
  border-radius: 20px;
  opacity: 0.2;
}
::-webkit-scrollbar-thumb {
  background-color: var(--p-surface-900);
  border-radius: 20px;
  height: 4px;
}

.group:hover::-webkit-scrollbar-thumb {
  background-color: var(--p-surface-800);
  border-radius: 20px;
  height: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: var(--p-surface-800);
}
</style>