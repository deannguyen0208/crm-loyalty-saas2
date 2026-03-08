import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createOrder, getOrders, seedOrders } from "../services/api";
import { useState } from "react";

export default function Orders() {
  const [form, setForm] = useState({ staff_name: "", item_name: "", quantity: 1, total_amount: 0, cost_amount: 0, payment_method: "momo" });
  const queryClient = useQueryClient();
  const { data } = useQuery({ queryKey: ["orders"], queryFn: getOrders });

  const createMutation = useMutation({
    mutationFn: createOrder,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["orders"] }),
  });

  const seedMutation = useMutation({
    mutationFn: seedOrders,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["orders", "overview"] }),
  });

  return (
    <div>
      <h1>Đơn hàng & thanh toán</h1>
      <div className="card">
        <input className="input" placeholder="Tên nhân viên" onChange={(e) => setForm({ ...form, staff_name: e.target.value })} />
        <input className="input" placeholder="Món" onChange={(e) => setForm({ ...form, item_name: e.target.value })} />
        <input className="input" type="number" placeholder="Số lượng" onChange={(e) => setForm({ ...form, quantity: Number(e.target.value) })} />
        <input className="input" type="number" placeholder="Doanh thu" onChange={(e) => setForm({ ...form, total_amount: Number(e.target.value) })} />
        <input className="input" type="number" placeholder="Chi phí" onChange={(e) => setForm({ ...form, cost_amount: Number(e.target.value) })} />
        <select className="input" onChange={(e) => setForm({ ...form, payment_method: e.target.value })}>
          <option value="momo">MOMO</option>
          <option value="zalopay">ZaloPay</option>
          <option value="bank_transfer">Tài khoản ngân hàng</option>
          <option value="cash">Tiền mặt</option>
        </select>
        <button className="btn primary" onClick={() => createMutation.mutate(form)}>Tạo đơn</button>
        <button className="btn" onClick={() => seedMutation.mutate()} style={{ marginLeft: 8 }}>Nạp dữ liệu demo</button>
      </div>
      <table className="table" style={{ marginTop: 12 }}>
        <thead><tr><th>Nhân sự</th><th>Món</th><th>Doanh thu</th><th>Thanh toán</th></tr></thead>
        <tbody>{data?.map((o) => <tr key={o.id}><td>{o.staff_name}</td><td>{o.item_name}</td><td>{o.total_amount}</td><td>{o.payment_method}</td></tr>)}</tbody>
      </table>
    </div>
  );
}
