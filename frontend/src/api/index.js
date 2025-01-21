import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export const fetchDepartments = () => axios.get(`${API_BASE_URL}/departments`);
export const fetchDoctors = () => axios.get(`${API_BASE_URL}/doctors`);
export const fetchPatients = () => axios.get(`${API_BASE_URL}/patients`);
export const fetchRegistrations = () => axios.get(`${API_BASE_URL}/registrations`);
export const addRegistration = (data) => axios.post(`${API_BASE_URL}/registrations`, data);
