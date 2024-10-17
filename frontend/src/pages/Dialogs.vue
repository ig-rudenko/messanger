<script setup lang="ts">
import {useStore} from "vuex";
import Toast from "primevue/toast";
import {Ref, ref, onMounted} from "vue";

import Profile from "@/components/Profile.vue";
import ChatDialog from "@/components/ChatDialog.vue";
import FindFriendship from "@/components/FindFriendship.vue";
import ChatTextInput from "@/components/ChatTextInput.vue";
import FriendshipEntityRow from "@/components/FriendshipEntityRow.vue";

import router from "@/router";
import {User} from "@/services/user";
import {newMessageToast} from "@/services/my.toast";
import WebSocketConnector from "@/services/websocket";
import {scrollChatContainerToEnd} from "@/services/scroller";
import {FriendshipEntityType, friendshipService} from "@/services/friendships";
import {ChatMessageType, chatService, handleMessage, RequestMessageType, ResponseMessageType} from "@/services/chats";
import {getAvatar} from "@/services/formats";

const store = useStore();
const user: User|null = store.state.auth.user;
if (!user) router.push("/auth/login");

// -------------------------------------------------------
let socket: WebSocketConnector|null = null;
const currentUserId = user?.id;
const openedDialogId: Ref<number> = ref(0);
const chatMessages: Ref<ChatMessageType[]|null> = ref(null);
// -------------------------------------------------------

// Создает всплывающее оповещение о новом сообщении.
async function notifyAboutNewMessage(message: ResponseMessageType) {
  let messageFrom = message.type + "ID: " + message.senderId;
  let messageFromAvatar = `${message.type} ${message.senderId}`;

  let from = friendshipService.getFriendshipById(message.senderId);

  if (!from) {
    from = await friendshipService.findFriendshipEntityById(message.senderId);
    if (!from) return;
    await friendshipService.createFriendship(from?.username);
  }

  from.lastMessage = message.message;
  from.lastDatetime = message.createdAt;
  from.newMessagesCount = (from.newMessagesCount || 0) + 1;

  messageFrom = `${from?.firstName||''} ${from?.lastName||''}`;
  messageFromAvatar = from?.image || "";
  newMessageToast(message.senderId, messageFrom, message.message, getAvatar(messageFrom, messageFromAvatar))
}

onMounted(() => {
  socket = new WebSocketConnector(`ws://${location.host}/ws`);

  socket.setOnMessage((ev: MessageEvent) => {
    handleMessage(ev.data).then(
        msg => {

          if (msg.type == "message") {
            // Добавляем в хранилище сообщение.
            chatService.appendMessageToChat(msg.senderId, msg);

            // Если открыт диалог с этим пользователем.
            if (msg.senderId == openedDialogId.value) {
              scrollChatContainerToEnd();
            } else {
              // Отображаем всплывающее оповещение.
              notifyAboutNewMessage(msg);
            }
          }

        }
    )

  })
})

// -------------------------------------------------------
friendshipService.getMyFriendships();

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
  scrollChatContainerToEnd();

  // Заправшиваем у сервера последние сообщения.
  chatService.getLastChatMessages(chat_id).then(value => {
    chatMessages.value = value;
    scrollChatContainerToEnd()
    // Убираем счетчик кол-ва новых непрочитанных сообщений.
    friendshipService.resetNewMessageCount(chat_id);
  })
}

// Добавление собственного сообщения в диалог.
function addMyMessageToChat(data: RequestMessageType) {
  // Если нет открытого диалога, то ничего не делаем.
  if (!openedDialogId.value || !currentUserId) return;

  // Создаем новое сообщение.
  const msg: ChatMessageType = {
    message: data.message,
    recipientId: data.recipientId,
    senderId: currentUserId,
    createdAt: (new Date()).getTime() / 1000
  }

  // Обновляем последнее сообщение в панели всех чатов
  friendshipService.updateLastMessageInfo(msg.recipientId, msg.message, msg.createdAt);

  // Добавляем сообщение в хранилище чата.
  chatService.appendMessageToChat(data.recipientId, msg);
  scrollChatContainerToEnd();
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

      <SplitterPanel class="flex flex-col relative" :size="25" :minSize="20">
        <div>
          <Profile/>
        </div>
        <div class="p-1">
          <FindFriendship @gotFriendship="gotFriendship" @selectedFriendship="selectedFriendship" />
        </div>
        <div class="overflow-y-auto">
          <FriendshipEntityRow :class="openedDialogId==friendship.id?'bg-gray-300 dark:bg-gray-800':''"
                 v-for="friendship in friendshipService.friendshipsOrderedList" :data="friendship" @click="openDialog(friendship.id)" />
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

  <Toast position="top-right" group="message">
    <template #message="slotProps">
      <div class="flex flex-col items-start flex-auto cursor-pointer" @click="openDialog(slotProps.message.detail.id)">
        <div class="flex items-center gap-2">
          <Avatar v-if="slotProps.message.detail.avatar" :image="slotProps.message.detail.avatar" shape="circle" />
          <span class="font-bold">{{slotProps.message.summary}}</span>
        </div>
        <div class="text-sm my-4" v-html="slotProps.message.detail.message"></div>
        <!--        <Button size="small" label="Reply" severity="success" @click="onReply()"></Button>-->
      </div>
    </template>
  </Toast>

</template>

<style scoped>

</style>