<script setup lang="ts">
import {useStore} from "vuex";
import {Ref, ref, onMounted} from "vue";

import Profile from "@/components/Profile.vue";
import ChatDialog from "@/components/ChatDialog.vue";
import FindFriendship from "@/components/FindFriendship.vue";
import ChatTextInput from "@/components/ChatTextInput.vue";
import FriendshipEntityRow from "@/components/FriendshipEntityRow.vue";

import router from "@/router";
import {User} from "@/services/user";
import {infoToast} from "@/services/my.toast";
import WebSocketConnector from "@/services/websocket";
import {scrollChatContainerToEnd} from "@/services/scroller";
import {FriendshipEntityType, friendshipService} from "@/services/friendships";
import {ChatMessageType, chatService, handleMessage, RequestMessageType} from "@/services/chats";

const store = useStore();
const user: User|null = store.state.auth.user;
if (!user) router.push("/auth/login");

// -------------------------------------------------------
let socket: WebSocketConnector|null = null;
const currentUserId = user?.id;
const openedDialogId: Ref<number> = ref(0);
const chatMessages: Ref<ChatMessageType[]|null> = ref(null);
const myFriendships: Ref<FriendshipEntityType[]> = ref([])

// -------------------------------------------------------
onMounted(() => {
  socket = new WebSocketConnector(`ws://${location.host}/ws`);

  socket.setOnMessage((ev: MessageEvent) => {
    handleMessage(ev.data).then(
        msg => {

          if (msg.type == "message") {
            // console.log(msg.senderId, openedDialogId.value)
            if (msg.senderId == openedDialogId.value) {
              if (chatMessages.value) {
                chatMessages.value.push(msg);
                scrollChatContainerToEnd();
              }
            } else {
              infoToast(msg.type, msg.message);
            }
          }

        }
    )

  })
})

// -------------------------------------------------------
friendshipService.getMyFriendships().then(value => myFriendships.value = value)

// Обработка новой дружеской связи.
function gotFriendship(friendship: FriendshipEntityType) {
  openDialog(friendship.id);
}

// Обработка выбора дружеской связи
function selectedFriendship(friendship: FriendshipEntityType) {
  openDialog(friendship.id);
}

// Обработка открытия диалога конкретного чата
function openDialog(chat_id: number) {
  if (openedDialogId.value == chat_id) return;

  openedDialogId.value = chat_id;
  // Сразу пытаемся заполнить сообщениями из хранилища.
  chatMessages.value = chatService.getStoredChat(chat_id);
  scrollChatContainerToEnd()

  // Заправшиваем у сервера последние сообщения.
  chatService.getLastChatMessages(chat_id).then(value => {
    chatMessages.value = value;
    scrollChatContainerToEnd()
  })
}

function addMyMessageToChat(data: RequestMessageType) {
  if (!openedDialogId.value || !chatMessages.value || !currentUserId) return;

  chatMessages.value.push(
      {
        message: data.message,
        recipientId: data.recipientId,
        senderId: currentUserId,
        createdAt: (new Date()).getTime() / 1000
      }
  )
  chatService.saveChat(data.recipientId, chatMessages.value)
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

      <SplitterPanel class="flex flex-col relative" :size="25" :minSize="10">
        <div>
          <Profile/>
        </div>
        <div class="p-1">
          <FindFriendship @gotFriendship="gotFriendship" @selectedFriendship="selectedFriendship" />
        </div>
        <div class="overflow-y-auto">
          <FriendshipEntityRow :class="openedDialogId==friendship.id?'bg-gray-300 dark:bg-gray-800':''"
                 v-for="friendship in myFriendships" :data="friendship" @click="openDialog(friendship.id)" />
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