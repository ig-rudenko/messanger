<script setup lang="ts">
import {useStore} from "vuex";
import Toast from "primevue/toast";
import {onMounted, ref, Ref} from "vue";

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

// -------------------------------------------------------
const isMobile: Ref<boolean> = ref(window.innerWidth < 640);
const showMobileMenu: Ref<boolean> = ref(true);
let user: User|null = null;
let socket: WebSocketConnector|null = null;
let currentUserId: number|null = null;
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
  newMessageToast(message.senderId, messageFrom, message.message, getAvatar(from.username, messageFromAvatar), 5000)
}

onMounted(() => {
  const store = useStore();
  user = store.state.auth.user;
  if (!user) router.push("/auth/login");

  currentUserId = user?.id || null;

  window.addEventListener("resize", () => {isMobile.value = window.innerWidth < 640 });

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
            }

            // Отображаем всплывающее оповещение.
            // Если не открыт диалог с этим пользователем, либо мобильная версия с открытым меню.
            if ((!isMobile.value && msg.senderId != openedDialogId.value) || (isMobile.value && showMobileMenu.value)) {
              notifyAboutNewMessage(msg);
            }
          }

          if (msg.type == "change_status") {
            const friendship = friendshipService.getFriendshipById(msg.senderId);
            if (friendship) friendship.online = msg.status == "online";
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
  // Выключаем мобильное окно.
  showMobileMenu.value = false;
  // Фокус на поле ввода.
  document.getElementById("chat-input")?.focus();
  if (openedDialogId.value == chat_id) return;

  openedDialogId.value = 0;
  openedDialogId.value = chat_id;
  
  setTimeout(() => {
    // Сразу пытаемся заполнить сообщениями из хранилища.
    chatMessages.value = chatService.getStoredChat(chat_id);
    scrollChatContainerToEnd(true);

    // Запрашиваем у сервера последние сообщения.
    chatService.getLastChatMessages(chat_id).then(value => {
      chatMessages.value = value;
      scrollChatContainerToEnd(true)
      // Убираем счетчик кол-ва новых непрочитанных сообщений.
      friendshipService.resetNewMessageCount(chat_id);
    })
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
    createdAt: Math.floor((new Date()).getTime())
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

    <label v-if="isMobile" for="showTopPanel" class="flex justify-start w-full p-2" style="height: 50px;">
      <input v-model="showMobileMenu" type="checkbox" name="showTopPanel" id="showTopPanel" hidden />
      <i class="pi pi-list dark:text-gray-200 text-2xl cursor-pointer p-2"/>
    </label>

    <Splitter class="h-full overflow-hidden" :class="isMobile?'!h-[calc(100vh-55px)]':''">

      <SplitterPanel
          v-show="!isMobile || isMobile && showMobileMenu"
          :class="isMobile?'!h-[calc(100vh-55px)]':''"
          class="flex w-full flex-col sm:relative absolute bg-surface-100 dark:bg-surface-900 h-full" :size="25">
        <div>
          <Profile :is-connected="socket?.isConnected.value"/>
        </div>
        <div class="p-1">
          <FindFriendship @gotFriendship="gotFriendship" @selectedFriendship="selectedFriendship" />
        </div>
        <div class="overflow-y-auto">
          <FriendshipEntityRow :class="openedDialogId==friendship.id?'bg-gray-300 dark:bg-gray-800':''"
                 v-for="friendship in friendshipService.friendshipsOrderedList" :data="friendship" @click="openDialog(friendship.id)" />
        </div>
      </SplitterPanel>

      <SplitterPanel class="flex items-center flex-col" :size="75">
        <template v-if="openedDialogId && chatMessages !== null">
          <ChatDialog :chat-id="openedDialogId" :chatMessages="chatMessages"
                      @view-message="ts => chatService.updateLastReadTime(openedDialogId, ts)"/>
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
        <div class="text-sm p-4" v-html="slotProps.message.detail.message"></div>
      </div>
    </template>
  </Toast>

</template>

<style scoped>

</style>