import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import './assets/styles.css'; // 可选的全局样式

const app = createApp(App);
app.use(router);
app.mount('#app');
