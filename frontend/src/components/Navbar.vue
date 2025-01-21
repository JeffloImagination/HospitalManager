<template>
    <nav>
      <ul>
        <li><router-link to="/home">首页</router-link></li>
        <li><router-link to="/departments">科室管理</router-link></li>
        <li><router-link to="/doctors">医生管理</router-link></li>
        <li><router-link to="/patients">患者管理</router-link></li>
        <li><router-link to="/registrations">挂号管理</router-link></li>
      </ul>
    </nav>
  </template>
  <style>
  nav ul {
    display: flex;
    list-style: none;
  }
  nav li {
    margin-right: 15px;
  }
  </style>
  