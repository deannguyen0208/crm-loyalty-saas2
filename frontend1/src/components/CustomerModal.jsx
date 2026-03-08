import { useState } from "react";

export default function CustomerModal({ isOpen, onClose, onSubmit }) {
  const [form, setForm] = useState({ name: "", phone: "", segment: "regular" });
  if (!isOpen) return null;

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,.45)", display: "grid", placeItems: "center" }}>
      <div className="card" style={{ width: 360 }}>
        <h3>Thêm khách hàng</h3>
        <input className="input" placeholder="Tên" onChange={(e) => setForm({ ...form, name: e.target.value })} />
        <input className="input" placeholder="Số điện thoại" onChange={(e) => setForm({ ...form, phone: e.target.value })} />
        <select className="input" onChange={(e) => setForm({ ...form, segment: e.target.value })}>
          <option value="regular">Regular</option>
          <option value="vip">VIP</option>
        </select>
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
          <button className="btn" onClick={onClose}>Huỷ</button>
          <button className="btn primary" onClick={() => onSubmit(form)}>Lưu</button>
        </div>
      </div>
    </div>
  );
}
