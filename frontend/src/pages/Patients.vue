<template>
  <div class="patients">
    <h1>患者管理</h1>

    <!-- 添加患者表单 -->
    <div class="add-patient-form">
      <h2>添加患者</h2>
      <form @submit.prevent="addPatient">
        <div>
          <label for="name">姓名：</label>
          <input v-model="newPatient.name" id="name" type="text" required />
        </div>
        <div>
          <label for="gender">性别：</label>
          <select v-model="newPatient.gender" id="gender" required>
            <option value="M">男</option>
            <option value="F">女</option>
          </select>
        </div>
        <div>
          <label for="phone">联系电话：</label>
          <input v-model="newPatient.phone" id="phone" type="text" required />
        </div>
        <div>
          <label for="doctor">主治医生：</label>
          <select v-model="newPatient.primary_doctor_id" id="doctor" required>
            <option v-if="doctors.length === 0" disabled>加载中...</option>
            <option v-for="doctor in doctors" :key="doctor.id" :value="doctor.id">
              {{ doctor.name }}（专长：{{ doctor.specialization }}）
            </option>
          </select>
        </div>
        <button type="submit">添加患者</button>
      </form>
    </div>

    <!-- 患者列表 -->
    <div class="patient-list">
      <h2>患者列表</h2>
      <table>
        <thead>
          <tr>
            <th>患者ID</th>
            <th>姓名</th>
            <th>性别</th>
            <th>联系电话</th>
            <th>主治医生</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="patient in patients" :key="patient.id">
            <td>{{ patient.id }}</td>
            <td>{{ patient.name }}</td>
            <td>{{ patient.gender === 'M' ? '男' : '女' }}</td>
            <td>{{ patient.phone }}</td>
            <td>{{ patient.doctor_name }}</td>
            <td>
              <button @click="deletePatient(patient.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页控件 -->
      <div class="pagination">
        <button :disabled="page === 1" @click="changePage(page - 1)">上一页</button>
        <span>第 {{ page }} 页 / 共 {{ totalPages }} 页</span>
        <button :disabled="page === totalPages" @click="changePage(page + 1)">下一页</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, ref } from "vue";
import axios from "axios";

// 定义类型
interface Patient {
  id: string;
  name: string;
  gender: "M" | "F";
  phone: string;
  doctor_name: string;
}

interface Doctor {
  id: string;
  name: string;
  specialization: string;
}

interface NewPatientForm {
  name: string;
  gender: "M" | "F";
  phone: string;
  primary_doctor_id: string | null;
}

export default defineComponent({
  name: "Patients",
  setup() {
    const patients = ref([]); // 患者数据
    const doctors = ref([]); // 医生数据
    const total = ref(0); // 总记录数
    const page = ref(1); // 当前页
    const perPage = ref(10); // 每页显示数量
    const totalPages = ref(1); // 总页数

    // 新增患者表单数据
    const newPatient = reactive<NewPatientForm>({
      name: "",
      gender: "M",
      phone: "",
      primary_doctor_id: null,
    });

    // 获取患者列表
    const fetchPatients = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/patients", {
          params: { page: page.value, per_page: perPage.value },
        });
        patients.value = response.data.patients;
        total.value = response.data.total;
        totalPages.value = Math.ceil(total.value / perPage.value);
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

    // 添加新患者
    const addPatient = async () => {
      try {
        await axios.post("http://127.0.0.1:5000/api/patients", newPatient);
        alert("患者添加成功！");
        // 重新获取患者列表
        await fetchPatients();
        // 清空表单
        newPatient.name = "";
        newPatient.gender = "M";
        newPatient.phone = "";
        newPatient.primary_doctor_id = null;
      } catch (error) {
        console.error("添加患者失败:", error);
        alert("添加患者失败，请检查数据！");
      }
    };

    // 删除患者
    const deletePatient = async (id: string) => {
      if (confirm("确定要删除该患者吗？")) {
        try {
          await axios.delete(`http://127.0.0.1:5000/api/patients/${id}`);
          alert("患者删除成功！");
          // 重新获取患者列表
          await fetchPatients();
        } catch (error) {
          console.error("删除患者失败:", error);
          alert("删除患者失败！");
        }
      }
    };

    const changePage = (newPage: number) => {
      page.value = newPage;
      fetchPatients();
    };

    // 组件挂载时调用
    onMounted(() => {
      fetchPatients();
      fetchDoctors();
    });

    return {
      patients,
      doctors,
      newPatient,
      addPatient,
      deletePatient,
      page,
      totalPages,
      changePage,
    };
  },
});
</script>

<style scoped>
.patients {
  padding: 20px;
}

.add-patient-form {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.add-patient-form form div {
  margin-bottom: 10px;
}

.add-patient-form label {
  display: inline-block;
  width: 100px;
}

.add-patient-form input,
.add-patient-form select {
  width: 200px;
  padding: 5px;
}

.patient-list table {
  width: 100%;
  border-collapse: collapse;
}

.patient-list th,
.patient-list td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

.patient-list th {
  background-color: #f4f4f4;
}

.pagination {
  margin-top: 15px;
  text-align: center;
}

.pagination button {
  margin: 0 10px;
  padding: 5px 10px;
  font-size: 14px;
  cursor: pointer;
}

.pagination button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
