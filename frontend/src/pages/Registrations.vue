<template>
  <div class="registrations">
    <h1>挂号管理</h1>

    <!-- 添加挂号表单 -->
    <div class="add-registration-form">
      <h2>新增挂号</h2>
      <form @submit.prevent="addRegistration">
        <div>
          <label for="patient">患者：</label>
          <select v-model="newRegistration.patient_id" id="patient" required>
            <option v-for="patient in patients" :key="patient.id" :value="patient.id">
              {{ patient.name }}
            </option>
          </select>
        </div>
        <div>
          <label for="doctor">医生：</label>
          <select v-model="newRegistration.doctor_id" id="doctor" required>
            <option v-for="doctor in doctors" :key="doctor.id" :value="doctor.id">
              {{ doctor.name }}
            </option>
          </select>
        </div>
        <div>
          <label for="department">科室：</label>
          <select v-model="newRegistration.department_id" id="department" required>
            <option v-for="department in departments" :key="department.id" :value="department.id">
              {{ department.name }}
            </option>
          </select>
        </div>
        <div>
          <label for="date">挂号日期：</label>
          <input v-model="newRegistration.registration_date" id="date" type="date" required />
        </div>
        <div>
          <label for="visit_type">就诊类型：</label>
          <select v-model="newRegistration.visit_type" id="visit_type" required>
            <option value="初诊">初诊</option>
            <option value="复诊">复诊</option>
          </select>
        </div>
        <button type="submit">新增挂号</button>
      </form>
    </div>

    <!-- 挂号列表 -->
    <div class="registration-list">
      <h2>挂号列表</h2>
      <table>
        <thead>
          <tr>
            <th>挂号单ID</th>
            <th>患者姓名</th>
            <th>医生姓名</th>
            <th>科室名称</th>
            <th>挂号日期</th>
            <th>就诊类型</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="registration in registrations" :key="registration.id">
            <td>{{ registration.id }}</td>
            <td>{{ registration.patient_name }}</td>
            <td>{{ registration.doctor_name }}</td>
            <td>{{ registration.department_name }}</td>
            <td>{{ registration.registration_date }}</td>
            <td>{{ registration.visit_type }}</td>
            <td>
              <button @click="deleteRegistration(registration.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- 分页控件 -->
      <div class="pagination">
        <button @click="prevPage" :disabled="page === 1">上一页</button>
        <span>第 {{ page }} 页 / 共 {{ totalPages }} 页</span>
        <button @click="nextPage" :disabled="page === totalPages">下一页</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, reactive } from "vue";
import axios from "axios";

// 定义类型
interface Patient {
  id: string;
  name: string;
}

interface Doctor {
  id: string;
  name: string;
}

interface Department {
  id: string;
  name: string;
}

interface NewRegistrationForm {
  patient_id: string;
  doctor_id: string;
  department_id: string;
  registration_date: string;
  visit_type: string;
}

interface Registration {
  id: string;
  patient_name: string;
  doctor_name: string;
  department_name: string;
  registration_date: string;
}

export default defineComponent({
  name: "Registrations",
  setup() {
    // 挂号数据
    const registrations = ref<Registration[]>([]);
    const patients = ref<Patient[]>([]);
    const doctors = ref<Doctor[]>([]);
    const departments = ref<Department[]>([]);
    const page = ref(1);
    const perPage = ref(10);
    const totalPages = ref(1);

    const newRegistration = reactive<NewRegistrationForm>({
      patient_id: "",
      doctor_id: "",
      department_id: "",
      registration_date: "",
      visit_type: "",
    });

    // 获取挂号数据
    const fetchRegistrations = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/registrations", {
          params: { page: page.value, per_page: perPage.value },
        });
        registrations.value = response.data.registrations;
        totalPages.value = Math.ceil(response.data.total / perPage.value);
      } catch (error) {
        console.error("获取挂号列表失败:", error);
      }
    };

    // 获取患者列表
    const fetchPatients = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/patients");
        patients.value = response.data.patients;
      } catch (error) {
        console.error("获取患者列表失败:", error);
      }
    };

    // 获取医生列表
    const fetchDoctors = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/doctors");
        doctors.value = response.data.doctors;
      } catch (error) {
        console.error("获取医生列表失败:", error);
      }
    };

    // 获取科室列表
    const fetchDepartments = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/departments");
        departments.value = response.data.departments;
      } catch (error) {
        console.error("获取科室列表失败:", error);
      }
    };

    // 添加新挂号记录
    const addRegistration = async () => {
      try {
        await axios.post("http://127.0.0.1:5000/api/registrations", newRegistration);
        alert("挂号成功！");
        // 重新获取挂号记录
        fetchRegistrations();
        // 清空表单
        newRegistration.patient_id = "";
        newRegistration.doctor_id = "";
        newRegistration.department_id = "";
        newRegistration.registration_date = "";
        newRegistration.visit_type = "";
      } catch (error) {
        console.error("添加挂号失败:", error);
        alert("添加挂号失败，请检查数据！");
      }
    };

    // 删除挂号记录
    const deleteRegistration = async (id: string) => {
      if (!confirm("确定要删除这条挂号记录吗？")) return;

      try {
        await axios.delete(`http://127.0.0.1:5000/api/registrations/${id}`);
        alert("挂号记录已删除！");
        fetchRegistrations();
      } catch (error) {
        console.error("删除挂号记录失败:", error);
        alert("删除挂号记录失败，请重试！");
      }
    };

    // 上一页
    const prevPage = () => {
      if (page.value > 1) {
        page.value--;
        fetchRegistrations();
      }
    };

    // 下一页
    const nextPage = () => {
      if (page.value < totalPages.value) {
        page.value++;
        fetchRegistrations();
      }
    };

    // 组件挂载时获取数据
    onMounted(() => {
      fetchRegistrations();
      fetchPatients();
      fetchDoctors();
      fetchDepartments();
    });

    return {
      registrations,
      patients,
      doctors,
      departments,
      newRegistration,
      addRegistration,
      deleteRegistration,
      page,
      totalPages,
      prevPage,
      nextPage,
    };
  },
});
</script>


<style scoped>
.registrations {
  padding: 20px;
}

.add-registration-form {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.add-registration-form form div {
  margin-bottom: 10px;
}

.add-registration-form label {
  display: inline-block;
  width: 120px;
}

.add-registration-form input,
.add-registration-form select {
  width: 200px;
  padding: 5px;
}
.registration-list table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 10px;
}

.registration-list th,
.registration-list td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.registration-list th {
  background-color: #f4f4f4;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination button {
  margin: 0 10px;
  padding: 5px 10px;
}
</style>
