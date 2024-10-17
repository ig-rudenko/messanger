<script setup lang="ts">
import {PropType} from "vue";

import {verboseDatetime} from "@/services/formats";
import {FriendshipEntityType} from "@/services/friendships";

const props = defineProps({
  data: {
    required: true,
    type: Object as PropType<FriendshipEntityType>
  }
})

function getAvatar() {
    if (props.data?.image) return props.data.image;
    return `https://ui-avatars.com/api/?size=32&name=${props.data.username}&font-size=0.33&background=random&rounded=true`
}

</script>

<template>
  <div v-ripple class="p-3 dark:bg-gray-700 dark:border-gray-900 border-b-2 first:border-y-2 flex gap-4 hover:bg-gray-200 dark:hover:bg-gray-900 cursor-pointer">
    <div class="flex items-baseline relative">
      <Avatar class="p-overlay-badge" :image="getAvatar()" shape="circle" size="large" />
      <div v-if="data.online">
        <div class="absolute p-[0.4rem] bg-green-500 rounded-full border-2 dark:border-gray-600 animate-ping -right-1 -bottom-1"></div>
        <div class="absolute p-[0.4rem] bg-green-500 rounded-full border-2 dark:border-gray-600 border-opacity-5 -right-1 -bottom-1"></div>
      </div>
    </div>
    <div class="w-full flex flex-col justify-center">
      <div class="flex justify-between">
        <span class="font-semibold">{{ data.firstName }} {{ data.lastName }}</span>
        <span v-if="data?.lastDatetime">{{ verboseDatetime(data.lastDatetime) }}</span>
      </div>
      <div v-if="data?.lastMessage" class="text-gray-500 dark:text-gray-400 w-0">
        <div class="w-max">
          {{ data.lastMessage }}
        </div>
      </div>
    </div>
  </div>
</template>
