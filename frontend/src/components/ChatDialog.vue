<script setup lang="ts">
import {ChatMessageType, chatService} from "@/services/chats";
import {onMounted, onUpdated, PropType} from "vue";
import ChatMessage from "@/components/ChatMessage.vue";
import {scrollChatContainerToEnd, scrollChatContainerToMessageByTime} from "@/services/scroller";
import {useStore} from "vuex";
import {User} from "@/services/user";

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

const emit = defineEmits(['viewMessage'])
let topViewMessageTime: number = 0;
let enableMessageLoaderScroller = true;

const observerOptions = {
  root: document.querySelector('.messages-container'),
  threshold: 0.15, // 15% сообщения должно быть видно на экране
};
const observerCallback = (entries: any) => {
  entries.forEach((entry: any) => {
    if (entry.isIntersecting) {
      const messageTimestamp = entry.target.attributes['data-created-at']?.value;
      if (messageTimestamp) {
        topViewMessageTime = Number(messageTimestamp);
        emit('viewMessage', topViewMessageTime);
      }
      if (enableMessageLoaderScroller && entry.target.attributes["mark"]?.value === "first") {
        enableMessageLoaderScroller = false;
        const lastTopViewMessageTime = topViewMessageTime;

        chatService.getChatMessages(props.chatId, messageTimestamp, 100).then(
            (messages: ChatMessageType[]) => {
              props.chatMessages?.unshift(...messages);
              scrollChatContainerToMessageByTime(lastTopViewMessageTime)
              setTimeout(() => enableMessageLoaderScroller = true, 500)
            }
        )

      }
    }
  });
};

const observer = new IntersectionObserver(observerCallback, observerOptions);

const store = useStore()
const user: User = store.state.auth.user!
const currentUserId = user.id

let lastReadTime = 0;


onMounted( async () => {
  scrollChatContainerToEnd();
  lastReadTime = await chatService.getLastReadTime(props.chatId);
})

onUpdated(async () => {
  const messages = document.querySelectorAll('.message');
  messages.forEach(message => observer.observe(message));
  lastReadTime = await chatService.getLastReadTime(props.chatId);
})

function showNewMessagesDivider(msg: ChatMessageType, index: number) {
  if (!lastReadTime) return false;

  const next = props.chatMessages[index + 1];

  return msg?.createdAt < lastReadTime && next?.createdAt > lastReadTime;

}

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

  const paddingTimeShift = 100 * 1000;

  // Если время между предыдущим сообщением и текущим больше paddingTimeShift ms, добавляем скругление.
  if (props.chatMessages[index - 1] && props.chatMessages[index].createdAt > (props.chatMessages[index - 1].createdAt + paddingTimeShift)) {
    classes.push(...["rounded-t-xl"])
  }
  // Если время между последующим сообщением и текущим больше paddingTimeShift ms, добавляем отступ и скругление.
  if (props.chatMessages[index + 1] && props.chatMessages[index + 1].createdAt > (props.chatMessages[index].createdAt + paddingTimeShift)) {
    classes.push(...["mb-10", "rounded-b-xl"])
  }

  return classes
}

</script>

<template>
  <div id="chat-dialog" v-if="chatMessages" class="w-full h-full flex flex-col-reverse overflow-y-auto">
    <div id="messages-container" class="group flex flex-col p-2 sm:p-10">
      <template v-for="(msg, index) in chatMessages">
        <ChatMessage :message="msg" :class="getMessageClasses(msg, index)" :mark="index===0?'first':''"/>

        <div id="unread-messages" v-if="showNewMessagesDivider(msg, index)" class="py-2">
          <hr>
          <div class="text-sm text-gray-600 dark:text-gray-400 flex justify-center">Новые</div>
        </div>

      </template>
    </div>
  </div>
</template>

<style scoped>
#chat-dialog::-webkit-scrollbar {
  display: inline;
  width: 6px;
  height: 5px;
}

#chat-dialog::-webkit-scrollbar-track-piece {
  background-color: var(--p-surface-0);
  border-radius: 20px;
  opacity: 0.2;
}

#chat-dialog:hover::-webkit-scrollbar-track-piece {
  background-color: var(--p-surface-200);
}

#chat-dialog::-webkit-scrollbar-thumb {
  background-color: var(--p-surface-0);
}

#chat-dialog:hover::-webkit-scrollbar-thumb {
  background-color: var(--p-surface-400);
  border-radius: 20px;
  height: 4px;
}

#chat-dialog::-webkit-scrollbar-thumb:hover {
  background-color: var(--p-surface-800);
}


#chat-dialog:where(.dark, .dark *)::-webkit-scrollbar-track-piece {
  background-color: var(--p-surface-900);
}

#chat-dialog:where(.dark, .dark *):hover::-webkit-scrollbar-track-piece {
  background-color: var(--p-surface-600);
}

#chat-dialog:where(.dark, .dark *)::-webkit-scrollbar-thumb {
  background-color: var(--p-surface-900);
}

#chat-dialog:where(.dark, .dark *):hover::-webkit-scrollbar-thumb {
  background-color: var(--p-surface-800);
}

#chat-dialog:where(.dark, .dark *)::-webkit-scrollbar-thumb:hover {
  background-color: var(--p-surface-400);
}
</style>