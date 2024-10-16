<script setup lang="ts">
import {ChatMessageType} from "@/services/chats";
import {onMounted, PropType} from "vue";
import ChatMessage from "@/components/ChatMessage.vue";
import {scrollChatContainerToEnd} from "@/services/scroller";
import {useStore} from "vuex";
import {User} from "@/services/user.ts";

const props = defineProps({
  chatId: {
    required: true,
    type: Number,
  },
  chatMessages: {
    required: true,
    type: Object as PropType<ChatMessageType[]>
  }
})

const store = useStore()
const user: User = store.state.auth.user!
const currentUserId = user.id

onMounted(() => {
  scrollChatContainerToEnd()
})

function getMessageClasses(msg: ChatMessageType, index: number): string[] {
  let classes = []
  if (!props.chatMessages[index - 1] || props.chatMessages[index - 1].senderId != msg.senderId) {
    classes.push("rounded-t-2xl")
  }
  if (!props.chatMessages[index + 1] || props.chatMessages[index + 1].senderId != msg.senderId) {
    classes.push("rounded-b-2xl")
  }
  if (msg.senderId == currentUserId) {
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