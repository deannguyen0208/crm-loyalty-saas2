import { useState } from "react";
import { login, register } from "../services/api";

export default function useAuth() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  const signIn = async (payload) => {
    const res = await login(payload);
    localStorage.setItem("token", res.access_token);
    setToken(res.access_token);
  };

  const signUp = async (payload) => {
    const res = await register(payload);
    localStorage.setItem("token", res.access_token);
    setToken(res.access_token);
  };

  return { token, signIn, signUp };
}
