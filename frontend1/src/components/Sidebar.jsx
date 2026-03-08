import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <h2>Cafe 100m² SaaS</h2>
      <p style={{ color: "#94a3b8", fontSize: 14 }}>Quản trị cho chủ quán nhỏ</p>
      <nav>
        <NavLink to="/">Dashboard</NavLink>
        <NavLink to="/customers">Khách hàng</NavLink>
        <NavLink to="/orders">Đơn hàng</NavLink>
        <NavLink to="/campaigns">Chiến dịch</NavLink>
      </nav>
    </aside>
  );
}
