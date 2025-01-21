import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Login from "../pages/Login.vue";
import Home from '../pages/Home.vue';
import Departments from '../pages/Departments.vue';
import Doctors from '../pages/Doctors.vue';
import Patients from '../pages/Patients.vue';
import Registrations from '../pages/Registrations.vue';

const routes: Array<RouteRecordRaw> = [
  { path: '/', redirect: "/login" },
  { path: '/login', component: Login},
  { path: '/home', component: Home},
  { path: '/departments', component: Departments },
  { path: '/doctors', component: Doctors },
  { path: '/patients', component: Patients },
  { path: '/registrations', component: Registrations },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
