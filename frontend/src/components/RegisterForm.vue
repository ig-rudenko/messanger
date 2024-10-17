<script lang="ts">
import {defineComponent} from 'vue'
import {mapActions, mapState} from "vuex";

import {RegisterUser} from "@/services/user";
import {AxiosError} from "axios";
import getVerboseAxiosError from "@/services/errorFmt";

export default defineComponent({
  name: "LoginForm",
  data() {
    return {
      user: new RegisterUser(),
      userError: "",
    };
  },
  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
      state: (state: any) => state,
    }),
  },
  created() {
    if (this.loggedIn) {
      this.$router.push("/");
    }
  },
  methods: {
    ...mapActions("auth", ["register"]),

    getClassesFor(isValid: boolean): string {
      return isValid ? '' : '!border-red-500'
    },
    handleRegister() {
      if (!this.user.isValid) return
      this.register(this.user)
          .then(() => this.$router.push("/auth/login"))
          .catch((reason: AxiosError<any>) => this.userError = getVerboseAxiosError(reason));
    },

  },
})
</script>

<template>
  <div class="p-4 shadow-2 border-round w-full lg:w-1/3 sm:w-2/3">
    <div class="text-center mb-5">
      <div class="text-900 text-3xl font-medium mb-3">Регистрация</div>
      <router-link to="/auth/login" class="font-medium no-underline ml-2 text-blue-500 cursor-pointer">У меня уже есть аккаунт</router-link>
    </div>

    <div class="flex flex-col gap-3">
      <div v-if="userError" class="flex justify-center pb-4">
        <Message class="select-none cursor-pointer" @click="userError = ''" severity="error" icon="pi pi-exclamation-triangle"><span v-html="userError"></span></Message>
      </div>

      <div>
<!--        USERNAME-->
        <InputText placeholder="Имя пользователя" @keydown.enter="handleRegister" v-model="user.username"
                   class="w-full !border-gray-400"
                   id="username-input" type="text" autofocus :class="getClassesFor(user.valid.username)" />
        <div class="px-1">
          <Message v-if="!user.valid.username" class="mt-1" severity="error"><span class="text-sm">{{user.valid.usernameError}}</span></Message>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-1">
        <div>
<!--          FIRST NAME-->
          <InputText placeholder="Имя" @keydown.enter="handleRegister" v-model="user.firstName"
                     class="w-full"
                     id="username-input" type="text" autofocus :class="getClassesFor(user.valid.firstName)" />
          <div class="px-1">
            <Message v-if="!user.valid.firstName" class="mt-1" severity="error"><span class="text-sm">{{user.valid.usernameError}}</span></Message>
          </div>
        </div>
        <div>
<!--          LAST NAME-->
          <InputText placeholder="Фамилия" @keydown.enter="handleRegister" v-model="user.lastName"
                     class="w-full"
                     id="username-input" type="text" autofocus :class="getClassesFor(user.valid.lastName)" />
          <div class="px-1">
            <Message v-if="!user.valid.lastName" class="mt-1" severity="error"><span class="text-sm">{{user.valid.usernameError}}</span></Message>
          </div>
        </div>
      </div>

      <div>
<!--        EMAIL-->
        <InputText placeholder="E-mail" @keydown.enter="handleRegister" v-model="user.email"
                   class="w-full !border-gray-400"
                   id="email-input" type="text" :class="getClassesFor(user.valid.email)" />
        <div class="px-1">
          <Message v-if="!user.valid.email" class="mt-1" severity="error"><span class="text-sm">{{user.valid.emailError}}</span></Message>
        </div>
      </div>

      <div>
<!--        PASSWORD-->
        <InputText placeholder="Пароль" @keydown.enter="handleRegister" v-model="user.password"
                   class="w-full !border-gray-400"
                   id="password1-input" type="password" :class="getClassesFor(user.valid.password)" />
        <div class="px-1">
          <Message v-if="!user.valid.password" class="mt-1" severity="error"><span class="text-sm">{{user.valid.passwordError}}</span></Message>
        </div>
      </div>

<!--      CONFIRM-->
      <InputText placeholder="Повторите пароль" @keydown.enter="handleRegister" v-model="user.password2"
                 class="w-full !border-gray-400"
                 id="password2-input" type="password" :class="getClassesFor(user.valid.password)" />

      <Button label="Зарегистрироваться" icon="pi pi-user" severity="info" @click="handleRegister" class="w-full"></Button>
    </div>
  </div>
</template>

<style scoped>

@media (width < 600px) {
  .shadow-2 {
    box-shadow: none!important;
  }
}
</style>