<script setup lang="ts">
import {onMounted} from "vue";
import {Ref, ref} from "vue";

import Profile from "@/components/Profile.vue";
import ChatDialog from "@/components/ChatDialog.vue";
import ChatElement from "@/components/ChatElement.vue";
import ChatTextInput from "@/components/ChatTextInput.vue";

import {infoToast} from "@/services/my.toast";
import WebSocketConnector from "@/services/websocket";
import {ChatElementType, ChatService, handleMessage, RequestMessageType} from "@/services/chats";

let socket: WebSocketConnector|null = null;

onMounted(() => {
  socket = new WebSocketConnector(`ws://${location.host}/ws`)

  socket.setOnMessage((ev: MessageEvent) => {
    handleMessage(ev.data).then(
        msg => infoToast(msg.type, msg.message)
    )

  })
})

const chatService = new ChatService()

const chats: Ref<ChatElementType[]> = ref([])
const openedDialogId: Ref<number> = ref(0)

chatService.getChats().then(value => chats.value = value)

function openDialog(id: number) {
  openedDialogId.value = id
}

function sendMessage(text: string) {
  const data: RequestMessageType = {
    type: "message",
    status: "new",
    recipientId: openedDialogId.value,
    message: text
  }
  if (socket) socket.sendMessage(data)
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
        <template v-if="openedDialogId">
          <ChatDialog :chat-id="openedDialogId" />
          <ChatTextInput @sendMessage="sendMessage"/>
        </template>
      </SplitterPanel>
    </Splitter>
  </div>
</template>

<style scoped>

</style>