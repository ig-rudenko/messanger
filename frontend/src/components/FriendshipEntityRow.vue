<script setup lang="ts">
import {PropType} from "vue";

import {getAvatar, verboseDatetime} from "@/services/formats";
import {FriendshipEntityType} from "@/services/friendships";

const props = defineProps({
  data: {
    required: true,
    type: Object as PropType<FriendshipEntityType>
  }
})

function getName(): string {
  let name = "";
  if (props.data?.firstName) name += props.data.firstName + " ";
  if (props.data?.lastName) name += props.data.lastName;
  if (!name.trim().length) name = "<span class='text-xs text-surface-400 font-mono pr-1'>id:</span>" + props.data.username;
  return name;
}

</script>

<template>
  <div v-ripple
       class="select-none p-3 dark:bg-gray-700 dark:border-gray-900 border-b-2 first:border-y-2 flex gap-4 hover:bg-gray-200 dark:hover:bg-gray-900 cursor-pointer">
    <div class="flex items-baseline relative">
      <Avatar class="p-overlay-badge" :image="getAvatar(props.data?.username, props.data?.image)" shape="circle"
              size="large"/>
      <div v-if="data.online">
        <div class="absolute p-[0.4rem] bg-green-500 rounded-full border-2 dark:border-gray-600 animate-ping -right-1 -bottom-1"></div>
        <div class="absolute p-[0.4rem] bg-green-500 rounded-full border-2 dark:border-gray-600 border-opacity-5 -right-1 -bottom-1"></div>
      </div>
    </div>
    <div class="w-full flex flex-col justify-center">
      <div class="flex justify-between">
        <div class="font-semibold"><span v-html="getName()"></span></div>

        <div v-if="data?.lastDatetime" class="flex flex-col">
          <div class="pl-2">{{ verboseDatetime(data.lastDatetime) }}</div>
          <div v-if="data?.newMessagesCount">
            <span class="bg-indigo-400 text-white w-fit px-2 animate-ping rounded-full absolute top-9">{{data.newMessagesCount}}</span>
            <span class="bg-indigo-400 text-white w-fit px-2 rounded-full absolute top-9">{{ data.newMessagesCount }}</span>
          </div>
        </div>
      </div>
      <div v-if="data?.lastMessage" class="text-gray-500 dark:text-gray-400 w-0">
        <div class="w-max">
          {{ data.lastMessage }}
        </div>
      </div>
    </div>
  </div>
</template>
