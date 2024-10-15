<script setup lang="ts">

import Profile from "@/components/Profile.vue";
import ChatElement from "@/components/ChatElement.vue";
import {ChatElementType, ChatService} from "@/services/chats.ts";
import {Ref, ref} from "vue";
import ChatDialog from "@/components/ChatDialog.vue";

const chatService = new ChatService()

const chats: Ref<ChatElementType[]> = ref([])
const openedDialogWith: Ref<string> = ref("")

chatService.getChats().then(value => chats.value = value)

function openDialog(username: string) {
  openedDialogWith.value = username
}

</script>

<template>
  <div style="height: 100vh;">
    <Splitter class="h-full">
      <SplitterPanel class="flex flex-col" :size="25" :minSize="10">
        <Profile/>
        <div class="overflow-y-auto">
          <ChatElement v-for="chat in chats" :chat="chat" @click="openDialog(chat.id)" />
        </div>
      </SplitterPanel>
      <SplitterPanel class="flex items-center justify-center" :size="75">
        <ChatDialog v-if="openedDialogWith" :chat-id="openedDialogWith" />
      </SplitterPanel>
    </Splitter>
  </div>
</template>

<style scoped>

</style>