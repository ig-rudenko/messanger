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
  let classes: string[] = []

  // Если сообщение от другого пользователя,
  if (!props.chatMessages[index - 1] || props.chatMessages[index - 1].senderId != msg.senderId) {
    classes.push("rounded-t-xl")
  }
  if (!props.chatMessages[index + 1] || props.chatMessages[index + 1].senderId != msg.senderId) {
    classes.push("rounded-b-xl")
  }
  if (msg.senderId == currentUserId) {
    classes.push(...["self-end", "bg-gray-200", "dark:bg-gray-700"])
  } else {
    classes.push(...["bg-indigo-200", "dark:bg-indigo-900"])
  }

  // Если время между предыдущим сообщением и текущим больше 100 сек, добавляем скругление.
  if (props.chatMessages[index - 1] && props.chatMessages[index].createdAt > (props.chatMessages[index - 1].createdAt + 100)) {
    classes.push(...["rounded-t-xl"])
  }
  // Если время между последующим сообщением и текущим больше 100 сек, добавляем отступ и скругление.
  if (props.chatMessages[index + 1] && props.chatMessages[index + 1].createdAt > (props.chatMessages[index].createdAt + 100)) {
    classes.push(...["mb-10", "rounded-b-xl"])
  }

  return classes
}

</script>

<template>
  <div v-if="chatMessages" class="group w-full h-full flex flex-col-reverse overflow-y-auto">
    <div id="messages-container" class="group flex flex-col p-10 ">
      <template v-for="(msg, index) in chatMessages">
        <ChatMessage :message="msg" :class="getMessageClasses(msg, index)"/>
      </template>
    </div>
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