<template>
  <div class="doctors">
    <h1>医生管理</h1>

    <!-- 添加医生表单 -->
    <div class="add-doctor-form">
      <h2>添加医生</h2>
      <form @submit.prevent="addDoctor">
        <div>
          <label for="id">工号：</label>
          <input v-model="newDoctor.id" id="id" type="text" required />
        </div>
        <div>
          <label for="name">姓名：</label>
          <input v-model="newDoctor.name" id="name" type="text" required />
        </div>
        <div>
          <label for="gender">性别：</label>
          <select v-model="newDoctor.gender" id="gender" required>
            <option value="M">男</option>
            <option value="F">女</option>
          </select>
        </div>
        <div>
          <label for="age">年龄：</label>
          <input v-model="newDoctor.age" id="age" type="number" required />
        </div>
        <div>
          <label for="phone">联系电话：</label>
          <input v-model="newDoctor.phone" id="phone" type="text" required />
        </div>
        <div>
          <label for="specialization">专长：</label>
          <input
            v-model="newDoctor.specialization"
            id="specialization"
            type="text"
            required
          />
        </div>
        <div>
          <label for="department">所属科室：</label>
          <select v-model="newDoctor.department_id" id="department" required>
            <option
              v-for="department in departments"
              :key="department.id"
              :value="department.id"
            >
              {{ department.name }}
            </option>
          </select>
        </div>
        <button type="submit">添加医生</button>
      </form>
    </div>

    <!-- 医生列表 -->
    <div class="doctor-list">
      <h2>医生列表</h2>
      <table>
        <thead>
          <tr>
            <th>工号</th>
            <th>姓名</th>
            <th>性别</th>
            <th>年龄</th>
            <th>联系电话</th>
            <th>专长</th>
            <th>所属科室</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doctor in doctors" :key="doctor.id">
            <td>{{ doctor.id }}</td>
            <td>{{ doctor.name }}</td>
            <td>{{ doctor.gender === 'M' ? '男' : '女' }}</td>
            <td>{{ doctor.age }}</td>
            <td>{{ doctor.phone }}</td>
            <td>{{ doctor.specialization }}</td>
            <td>{{ doctor.department_name }}</td>
            <td>
              <button @click="deleteDoctor(doctor.id)">删除</button>
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
import { defineComponent, ref, reactive, onMounted } from "vue";
import axios from "axios";

// 定义类型
interface Department {
  id: string;
  name: string;
  phone: string;
}

interface NewDoctorForm {
  id: string;
  name: string;
  gender: string;
  age: number;
  phone: string;
  specialization: string;
  department_id: string | null;
}

export default defineComponent({
  name: "Doctors",
  setup() {
    const doctors = ref([]);
    const departments = ref([]);
    const total = ref(0);
    const page = ref(1);
    const perPage = ref(10);
    const totalPages = ref(1);

    // 新增医生表单数据
    const newDoctor = reactive<NewDoctorForm>({
      id: "",
      name: "",
      gender: "M",
      age: null,
      phone: "",
      specialization: "",
      department_id: null,
    });

    // 获取医生列表
    const fetchDoctors = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/doctors", {
          params: { page: page.value, per_page: perPage.value },
        });
        doctors.value = response.data.doctors;
        total.value = response.data.total;
        totalPages.value = Math.ceil(total.value / perPage.value);
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

    // 添加新医生
    const addDoctor = async () => {
      try {
        await axios.post("http://127.0.0.1:5000/api/doctors", newDoctor);
        alert("医生添加成功！");
        // 重新获取医生列表
        fetchDoctors();
        // 清空表单
        newDoctor.id = "";
        newDoctor.name = "";
        newDoctor.gender = "M";
        newDoctor.age = null;
        newDoctor.phone = "";
        newDoctor.specialization = "";
        newDoctor.department_id = null;
      } catch (error) {
        console.error("添加医生失败:", error);
        alert("添加医生失败，请检查数据！");
      }
    };

    // 删除医生
    const deleteDoctor = async (id: string) => {
      if (confirm("确定要删除该医生吗？")) {
        try {
          await axios.delete(`http://127.0.0.1:5000/api/doctors/${id}`);
          alert("医生删除成功！");
          fetchDoctors(); // 删除成功后刷新列表
        } catch (error) {
          console.error("删除医生失败:", error);
          alert("删除医生失败，请重试！");
        }
      }
    };

    const changePage = (newPage: number) => {
      page.value = newPage;
      fetchDoctors();
    };

    onMounted(() => {
      fetchDoctors();
      fetchDepartments();
    });

    return {
      doctors,
      departments,
      newDoctor,
      addDoctor,
      deleteDoctor,
      page,
      totalPages,
      changePage,
    };
  },
});
</script>

<style scoped>
.doctors {
  padding: 20px;
}

.add-doctor-form {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.add-doctor-form form div {
  margin-bottom: 10px;
}

.add-doctor-form label {
  display: inline-block;
  width: 120px;
}

.add-doctor-form input,
.add-doctor-form select {
  width: 200px;
  padding: 5px;
}

.doctor-list table {
  width: 100%;
  border-collapse: collapse;
}

.doctor-list th,
.doctor-list td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

.doctor-list th {
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
