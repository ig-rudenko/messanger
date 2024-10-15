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

    getClassesFor(isValid: boolean): string[] {
      return isValid ? ['w-full', 'pb-3'] : ['w-full', 'pb-3', 'p-invalid']
    },
    handleRegister() {
      this.register(this.user)
          .then(() => this.$router.push("/login"))
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

    <div>
      <div v-if="userError" class="flex justify-center pb-4">
        <Message @click="userError = ''" severity="error" icon="pi pi-exclamation-triangle"><span v-html="userError"></span></Message>
      </div>

      <div class="mb-5">
        <FloatLabel>
          <InputText @keydown.enter="handleRegister" v-model="user.username" id="username-input" type="text" autofocus :class="getClassesFor(user.valid.username)" />
          <label for="username-input" class="block text-900 mb-2">Username</label>
        </FloatLabel>
        <Message v-if="!user.valid.username" severity="error">{{user.valid.usernameError}}</Message>
      </div>

      <div class="mb-5">
        <FloatLabel>
          <InputText @keydown.enter="handleRegister" v-model="user.email" id="email-input" type="text" :class="getClassesFor(user.valid.email)" />
          <label for="email-input" class="block text-900 mb-2">Email</label>
        </FloatLabel>
        <Message v-if="!user.valid.email" severity="error">{{user.valid.emailError}}</Message>
      </div>

      <div class="mb-5">
        <FloatLabel>
          <InputText @keydown.enter="handleRegister" v-model="user.password" id="password1-input" type="password" :class="getClassesFor(user.valid.password)" />
          <label for="password1-input" class="block text-900 mb-2">Password</label>
        </FloatLabel>
        <Message v-if="!user.valid.password" severity="error">{{user.valid.passwordError}}</Message>
      </div>

      <FloatLabel class="mb-5">
        <InputText @keydown.enter="handleRegister" v-model="user.password2" id="password2-input" type="password" :class="getClassesFor(user.valid.password)" />
        <label for="password2-input" class="block text-900 mb-2">Confirm password</label>
      </FloatLabel>

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