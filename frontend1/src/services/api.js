import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
});

export const getCustomers = () => api.get("/customers").then((res) => res.data);
export const createCustomer = (data) => api.post("/customers", data).then((res) => res.data);
export const getOrders = () => api.get("/orders").then((res) => res.data);
export const createOrder = (data) => api.post("/orders", data).then((res) => res.data);
export const seedOrders = () => api.post("/orders/seed-demo").then((res) => res.data);
export const getOverview = () => api.get("/dashboard/overview").then((res) => res.data);
export const getCampaigns = () => api.get("/campaigns").then((res) => res.data);
export const login = (data) => api.post("/auth/login", data).then((res) => res.data);
export const register = (data) => api.post("/auth/register", data).then((res) => res.data);
