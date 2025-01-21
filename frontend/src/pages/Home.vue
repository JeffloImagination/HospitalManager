<!-- <template>
  <div class="home">
    <h1>前后端连接测试</h1>
    <p v-if="loading">正在连接后端...</p>
    <p v-else-if="error">{{ error }}</p>
    <p v-else>{{ message }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import axios from "axios";

export default defineComponent({
  name: "Home",
  setup() {
    const loading = ref(true);
    const error = ref<string | null>(null);
    const message = ref<string>("");

    // 测试 API 连接
    onMounted(async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/test-db");
        message.value = response.data.message;
      } catch (err: any) {
        error.value = "无法连接后端，请检查网络和后端状态";
      } finally {
        loading.value = false;
      }
    });

    return {
      loading,
      error,
      message,
    };
  },
});
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}

p {
  font-size: 18px;
  color: #333;
}
</style> -->

<template>
  <div class="home">
    <!--h1>小型医院挂号系统</h1>
    <div class="nav-links">
      <router-link to="/departments">科室管理</router-link>
      <router-link to="/doctors">医生管理</router-link>
      <router-link to="/patients">患者管理</router-link>
      <router-link to="/registrations">挂号管理</router-link>
    </div-->

    <div class="stats">
      <h2>系统概况</h2>
      <div class="stat-item">
        <p>科室数</p>
        <span>{{ departmentCount }}</span>
      </div>
      <div class="stat-item">
        <p>医生数</p>
        <span>{{ doctorCount }}</span>
      </div>
      <div class="stat-item">
        <p>患者数</p>
        <span>{{ patientCount }}</span>
      </div>
      <div class="stat-item">
        <p>挂号数</p>
        <span>{{ registrationCount }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import axios from "axios";

export default defineComponent({
  name: "Home",
  setup() {
    // 定义状态变量
    const departmentCount = ref<number>(0);
    const doctorCount = ref<number>(0);
    const patientCount = ref<number>(0);
    const registrationCount = ref<number>(0);

    // 定义获取数据的函数
    const fetchStats = async () => {
      try {
        // 发起后端请求获取统计数据
        const response = await axios.get("http://127.0.0.1:5000/api/stats");
        const data = response.data;

        // 更新状态
        departmentCount.value = data.departments;
        doctorCount.value = data.doctors;
        patientCount.value = data.patients;
        registrationCount.value = data.registrations;
      } catch (error) {
        console.error("获取统计数据失败:", error);
      }
    };

    // 组件挂载时调用
    onMounted(() => {
      fetchStats();
    });

    return {
      departmentCount,
      doctorCount,
      patientCount,
      registrationCount,
    };
  },
});
</script>

<style scoped>
.home {
  padding: 20px;
}

.nav-links {
  margin-bottom: 20px;
}

.nav-links a {
  margin-right: 15px;
  text-decoration: none;
  color: #007bff;
}

.nav-links a:hover {
  text-decoration: underline;
}

.stats {
  margin-top: 10px;
}

.stat-item {
  margin-bottom: 25px;
  display: flex;
  justify-content: space-between;
  font-size: 18px;
}

.stat-item p {
  margin: 0;
}
</style>
