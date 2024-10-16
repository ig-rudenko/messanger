<script lang="ts">
import {defineComponent} from 'vue'
import {mapState, mapActions} from "vuex";

import {LoginUser} from "@/services/user";
import {AxiosError, AxiosResponse} from "axios";
import getVerboseAxiosError from "@/services/errorFmt";

export default defineComponent({
  name: "LoginForm",

  data() {
    return {
      user: new LoginUser(),
      userError: "",
    };
  },
  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
    }),
  },
  created() {
    if (this.loggedIn) {
      this.$router.push("/");
    }
  },
  methods: {
    ...mapActions("auth", ["login"]),

    getClassesFor(isValid: boolean): string[] {
      return isValid ? ['w-full', 'pb-3'] : ['w-full', 'pb-3', 'p-invalid']
    },

    handleLogin() {
      this.login(this.user)
          .then(
              (value: AxiosResponse|AxiosError) => {
                if (value.status != 200) {
                  this.userError = (<AxiosError>value).message
                }
              },
              () => this.userError = 'Неверный логин или пароль'
          )
          .catch(
          (reason: AxiosError<any>) => {
            this.userError = getVerboseAxiosError(reason)
          }
      );
    },
  },
})
</script>

<template>
  <div class="p-4 shadow-2 border-round w-full lg:w-1/3 sm:w-2/3">
    <div class="text-center mb-5">
      <div class="text-900 text-3xl font-medium mb-3">Добро пожаловать</div>
      <span class="text-600 font-medium line-height-3">Нет аккаунта?</span>
      <router-link to="/auth/signup" class="font-medium no-underline ml-2 text-blue-500 cursor-pointer">Создать</router-link>
    </div>

    <div>
      <div v-if="userError.length" class="flex justify-center mb-5">
        <Message @click="userError = ''" severity="error" icon="pi pi-exclamation-triangle"><span v-html="userError"></span></Message>
      </div>

      <div class="mb-5">
        <FloatLabel>
          <InputText @keydown.enter="handleLogin" v-model="user.username" id="username-input" type="text" autofocus :class="getClassesFor(user.valid.username)" />
          <label for="username-input" class="block text-900 mb-2">Username</label>
        </FloatLabel>
      </div>

      <div class="mb-5">
        <FloatLabel>
          <InputText @keydown.enter="handleLogin" v-model="user.password" id="password-input" type="password" :class="getClassesFor(user.valid.password)" />
          <label for="password-input" class="block text-900 mb-2">Password</label>
        </FloatLabel>
      </div>

      <Button label="Войти" icon="pi pi-user" :severity="'success'" @click="handleLogin" class="w-full"></Button>
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