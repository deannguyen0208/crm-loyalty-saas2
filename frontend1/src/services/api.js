import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true, // để gửi cookie chứa JWT
});

export const getCustomers = () => api.get("/customers").then((res) => res.data);
export const createCustomer = (data) =>
  api.post("/customers", data).then((res) => res.data);
// ... các hàm khác
