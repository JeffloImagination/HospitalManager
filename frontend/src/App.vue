<template>
  <div id="app">
    <header>
      <h1>小型医院挂号系统</h1>
      <nav>
        <router-link to="/home">首页</router-link>
        <router-link to="/departments">科室管理</router-link>
        <router-link to="/doctors">医生管理</router-link>
        <router-link to="/patients">患者管理</router-link>
        <router-link to="/registrations">挂号管理</router-link>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
    <footer>
      <p>© 2024 小型医院挂号系统</p>
    </footer>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
</script>

<style src="./assets/styles.css"></style>
