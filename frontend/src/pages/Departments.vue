<template>
  <div class="departments">
    <h1>科室管理</h1>

    <!-- 添加科室表单 -->
    <div class="add-department-form">
      <h2>添加科室</h2>
      <form @submit.prevent="addDepartment">
        <div>
          <label for="id">科室号：</label>
          <input v-model="newDepartment.id" id="id" type="text" required />
        </div>
        <div>
          <label for="name">科室名称：</label>
          <input v-model="newDepartment.name" id="name" type="text" required />
        </div>
        <div>
          <label for="phone">联系电话：</label>
          <input v-model="newDepartment.phone" id="phone" type="text" required />
        </div>
        <button type="submit">添加科室</button>
      </form>
    </div>

    <!-- 科室列表 -->
    <div class="department-list">
      <h2>科室列表</h2>
      <table>
        <thead>
          <tr>
            <th>科室号</th>
            <th>名称</th>
            <th>科室电话</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="department in departments" :key="department.id">
            <td>{{ department.id }}</td>
            <td>{{ department.name }}</td>
            <td>{{ department.phone }}</td>
            <td>
              <button @click="deleteDepartment(department.id)">删除</button>
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
interface NewDepartmentForm {
  id: string;
  name: string;
  phone: string;
}

export default defineComponent({
  name: "Departments",
  setup() {
    const departments = ref([]);
    const total = ref(0);
    const page = ref(1);
    const perPage = ref(10);
    const totalPages = ref(1);

    // 新增科室表单数据
    const newDepartment = reactive<NewDepartmentForm>({
      id: "",
      name: "",
      phone: "",
    });

    const fetchDepartments = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/departments", {
          params: { page: page.value, per_page: perPage.value },
        });
        departments.value = response.data.departments;
        total.value = response.data.total;
        totalPages.value = Math.ceil(total.value / perPage.value);
      } catch (error) {
        console.error("获取科室列表失败:", error);
      }
    };

    // 添加新科室
    const addDepartment = async () => {
      try {
        await axios.post("http://127.0.0.1:5000/api/departments", newDepartment);
        alert("科室添加成功！");
        // 重新获取科室列表
        fetchDepartments();
        // 清空表单
        newDepartment.id = "";
        newDepartment.name = "";
        newDepartment.phone = "";
      } catch (error) {
        console.error("添加科室失败:", error);
        alert("添加科室失败，请检查数据！");
      }
    };

    // 删除科室
    const deleteDepartment = async (id: string) => {
      if (confirm("确认要删除该科室吗？")) {
        try {
          await axios.delete(`http://127.0.0.1:5000/api/departments/${id}`);
          alert("科室删除成功！");
          fetchDepartments();
        } catch (error) {
          console.error("删除科室失败:", error);
          alert("删除科室失败，请稍后重试！");
        }
      }
    };

    const changePage = (newPage: number) => {
      page.value = newPage;
      fetchDepartments();
    };

    onMounted(() => {
      fetchDepartments();
    });

    return {
      departments,
      newDepartment,
      addDepartment,
      deleteDepartment,
      page,
      totalPages,
      changePage,
    };
  },
});
</script>

<style scoped>
.departments {
  padding: 20px;
}

.add-department-form {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.add-department-form form div {
  margin-bottom: 10px;
}

.add-department-form label {
  display: inline-block;
  width: 100px;
}

.add-department-form input {
  width: 200px;
  padding: 5px;
}

.department-list table {
  width: 100%;
  border-collapse: collapse;
}

.department-list th,
.department-list td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

.department-list th {
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
