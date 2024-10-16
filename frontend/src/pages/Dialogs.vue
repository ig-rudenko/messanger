<script setup lang="ts">
import {onMounted} from "vue";
import {Ref, ref} from "vue";

import Profile from "@/components/Profile.vue";
import ChatDialog from "@/components/ChatDialog.vue";
import ChatElement from "@/components/ChatElement.vue";
import ChatTextInput from "@/components/ChatTextInput.vue";

import {infoToast} from "@/services/my.toast";
import WebSocketConnector from "@/services/websocket";
import {ChatElementType, ChatMessageType, ChatService, handleMessage, RequestMessageType} from "@/services/chats";
import {scrollChatContainerToEnd} from "@/services/scroller.ts";
import {useStore} from "vuex";
import {User} from "@/services/user.ts";
import router from "@/router.ts";

let socket: WebSocketConnector|null = null;
const store = useStore()
const user: User|null = store.state.auth.user

if (!user) router.push("/auth/login");

const currentUserId = user?.id

onMounted(() => {
  socket = new WebSocketConnector(`ws://${location.host}/ws`)

  socket.setOnMessage((ev: MessageEvent) => {
    handleMessage(ev.data).then(
        msg => {

          if (msg.type == "message") {
            console.log(msg.senderId, openedDialogId.value)
            if (msg.senderId == openedDialogId.value) {
              if (chatMessages.value) {
                chatMessages.value.push(msg)
                scrollChatContainerToEnd()
              }
            } else {
              infoToast(msg.type, msg.message);
            }
          }

        }
    )

  })
})

const chatService = new ChatService()

const chats: Ref<ChatElementType[]> = ref([])
chatService.getChats().then(value => chats.value = value)

const chatMessages: Ref<ChatMessageType[]|null> = ref(null)

const openedDialogId: Ref<number> = ref(0)
function openDialog(id: number) {
  if (openedDialogId.value == id) return;

  openedDialogId.value = id;
  chatMessages.value = null;

  chatService.getChatMessages(id).then(value => {
    chatMessages.value = value;
  })
}


function addMyMessageToChat(data: RequestMessageType) {
  if (!openedDialogId.value || !chatMessages.value) return;

  chatMessages.value.push(
      {
        message: data.message,
        recipientId: data.recipientId,
        senderId: currentUserId,
        createdAt: (new Date()).getTime()
      }
  )
  scrollChatContainerToEnd()
}

function sendMessage(text: string) {
  const data: RequestMessageType = {
    type: "message",
    status: "new",
    recipientId: openedDialogId.value,
    message: text
  }
  if (socket) {
    socket.sendMessage(data);
    addMyMessageToChat(data);
  }
}

</script>

<template>
  <div style="height: 100vh;">
    <Splitter class="h-full">
      <SplitterPanel class="flex flex-col" :size="25" :minSize="10">
        <Profile/>
        <div class="overflow-y-auto">
          <ChatElement :class="openedDialogId==chat.id?'bg-gray-300 dark:bg-gray-800':''"
                       v-for="chat in chats" :chat="chat" @click="openDialog(chat.id)" />
        </div>
      </SplitterPanel>
      <SplitterPanel class="flex items-center flex-col justify-center" :size="75">
        <template v-if="openedDialogId && chatMessages !== null">
          <ChatDialog :chat-id="openedDialogId" :chatMessages="chatMessages" />
          <ChatTextInput @sendMessage="sendMessage"/>
        </template>
      </SplitterPanel>
    </Splitter>
  </div>
</template>

<style scoped>

</style>