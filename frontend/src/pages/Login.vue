<template>
    <div class="login">
      <h1>医院挂号系统 - 登录</h1>
      <form @submit.prevent="login">
        <div>
          <label for="username">用户名：</label>
          <input id="username" v-model="username" type="text" required />
        </div>
        <div>
          <label for="password">密码：</label>
          <input id="password" v-model="password" type="password" required />
        </div>
        <button type="submit">登录</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  import axios from "axios";
  import { useRouter } from "vue-router";
  
  export default defineComponent({
    name: "Login",
    setup() {
      const username = ref("");
      const password = ref("");
      const errorMessage = ref("");
      const router = useRouter();
  
      const login = async () => {
        try {
          const response = await axios.post("http://127.0.0.1:5000/api/login", {
            username: username.value,
            password: password.value,
          });
          const role = response.data.role;
  
          // 根据角色跳转到不同页面
          if (role === "admin") {
            router.push("/departments");
          } else if (role === "doctor") {
            router.push("/patients");
          } else if (role === "patient") {
            router.push("/registrations");
          }
        } catch (error) {
          errorMessage.value = "用户名或密码错误，请重试！";
        }
      };
  
      return {
        username,
        password,
        login,
        errorMessage,
      };
    },
  });
  </script>
  
  <style scoped>
  .login {
    max-width: 400px;
    margin: 100px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    text-align: center;
  }
  
  .login form div {
    margin-bottom: 15px;
  }
  
  .login label {
    display: inline-block;
    width: 80px;
    text-align: right;
  }
  
  .login input {
    width: 200px;
    padding: 5px;
  }
  
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>
  