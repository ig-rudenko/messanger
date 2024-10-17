<script setup lang="ts">
import {Ref, ref} from "vue";
import {FriendshipEntityType, friendshipService} from "@/services/friendships.ts";
import FriendshipEntityRow from "@/components/FriendshipEntityRow.vue";

const visible = ref(false);
const search = ref("");

const newFriendships: Ref<FriendshipEntityType[]> = ref([]);
const emits = defineEmits(["gotFriendship", "selectedFriendship"])

function findFriendships() {
  if (search.value.length <= 3) return;
  friendshipService.findFriendship(search.value).then(
      value => newFriendships.value = value
  )
}

function isAlreadyHasFriendship(id: number): boolean {
  return friendshipService.getFriendshipById(id) != null;
}

function clickFriendship(username: string) {
  const friendship = friendshipService.getFriendshipByUsername(username)
  // Если уже дружим, то пропускаем.
  if (friendship) {
    emits("selectedFriendship", friendship);
    return
  }

  // Создаем дружбу.
  friendshipService.createFriendship(username).then(
      value => {
        emits("gotFriendship", value);
      }
  )
}

</script>

<template>
  <div>
    <!--  <Button icon="pi pi-search" @click="visible=!visible"/>-->
    <input class="rounded-2xl px-3 py-1 text-sm w-full bg-transparent active:border-0 focus:border-0 focus:outline-none"
           @keyup="() => !search.length?newFriendships=[]:''"
           v-model="search" @keydown.enter="findFriendships" placeholder="Поиск людей"/>
  </div>

  <div class="overflow-y-auto">
    <div v-for="friendship in newFriendships" class="relative group">
      <FriendshipEntityRow :data="friendship"
                           v-tooltip="isAlreadyHasFriendship(friendship.id)?'Открыть чат':'Дружить'"
                           @click="() => clickFriendship(friendship.username)"
                           class="hover:ring-2 ring-inset" />
      <i v-if="!isAlreadyHasFriendship(friendship.id)" class="pi pi-user-plus absolute right-5 top-8"/>
    </div>
  </div>

  <Dialog v-model:visible="visible" modal header="Edit Profile" pt:root:class="!border-0 !bg-transparent"
          pt:mask:class="backdrop-blur-sm">
    <span class="text-surface-500 dark:text-surface-400 block mb-8">Update your information.</span>
    <div class="flex items-center gap-4 mb-4">
      <label for="username" class="font-semibold w-24">Username</label>
      <InputText id="username" class="flex-auto" autocomplete="off"/>
    </div>
    <div class="flex items-center gap-4 mb-8">
      <label for="email" class="font-semibold w-24">Email</label>
      <InputText id="email" class="flex-auto" autocomplete="off"/>
    </div>
    <div class="flex justify-end gap-2">
      <Button type="button" label="Cancel" severity="secondary" @click="visible = false"></Button>
      <Button type="button" label="Save" @click="visible = false"></Button>
    </div>
  </Dialog>

</template>

<style scoped>

</style>