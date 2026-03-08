import { useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function Login() {
  const nav = useNavigate();
  const { signIn, signUp } = useAuth();
  const [isRegister, setRegister] = useState(false);
  const [form, setForm] = useState({ identifier: "", password: "", email: "", phone: "", full_name: "" });

  const submit = async () => {
    if (isRegister) {
      await signUp({ email: form.email, phone: form.phone, password: form.password, full_name: form.full_name });
    } else {
      await signIn({ identifier: form.identifier, password: form.password });
    }
    nav("/");
  };

  return (
    <div style={{ maxWidth: 380, margin: "80px auto" }} className="card">
      <h2>{isRegister ? "Đăng ký" : "Đăng nhập"}</h2>
      {isRegister ? (
        <>
          <input className="input" placeholder="Họ tên" onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          <input className="input" placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input className="input" placeholder="Số điện thoại" onChange={(e) => setForm({ ...form, phone: e.target.value })} />
        </>
      ) : <input className="input" placeholder="Email/SĐT" onChange={(e) => setForm({ ...form, identifier: e.target.value })} />}
      <input className="input" type="password" placeholder="Mật khẩu mạnh" onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <button className="btn primary" onClick={submit}>Tiếp tục</button>
      <button className="btn" onClick={() => setRegister(!isRegister)} style={{ marginLeft: 8 }}>
        {isRegister ? "Đã có tài khoản" : "Tạo tài khoản"}
      </button>
    </div>
  );
}
