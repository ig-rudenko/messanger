<script setup lang="ts">

</script>

<template>
<div class="p-3 border-b-2 flex flex-wrap justify-between items-center gap-4 bg-gray-300">
  <div class="flex flex-wrap items-center gap-4">
    <Avatar image="https://primefaces.org/cdn/primevue/images/organization/walter.jpg" class="mr-2" size="xlarge" shape="circle" />
    <div>
      <div class="text-xl font-semibold">Игорь Руденко</div>
    </div>
  </div>
  <div>
    <Button icon="pi pi-cog" text/>
    <Button v-tooltip.bottom="'Выйти'" icon="pi pi-sign-out" class="hover:text-red-600 hover:bg-red-100 bg-opacity-10" text/>
  </div>
</div>

</template>

<style scoped>

</style>