import { useQuery } from "@tanstack/react-query";
import { getOverview } from "../services/api";

export default function Dashboard() {
  const { data, isLoading } = useQuery({ queryKey: ["overview"], queryFn: getOverview });

  if (isLoading) return <p>Đang tải dashboard...</p>;

  return (
    <div>
      <h1>Tổng quan kinh doanh quán cafe</h1>
      <div className="grid">
        <div className="card"><h3>Doanh thu</h3><p>{data.summary.revenue.toLocaleString()} đ</p></div>
        <div className="card"><h3>Lợi nhuận</h3><p>{data.summary.profit.toLocaleString()} đ</p></div>
        <div className="card"><h3>Biên lợi nhuận</h3><p>{data.summary.margin}%</p></div>
        <div className="card"><h3>Số đơn</h3><p>{data.summary.orders}</p></div>
      </div>

      <div className="grid" style={{ marginTop: 12 }}>
        <div className="card">
          <h3>Best sellers</h3>
          {data.best_sellers.map((s) => <p key={s.item}>{s.item}: {s.revenue.toLocaleString()} đ</p>)}
        </div>
        <div className="card">
          <h3>Thanh toán</h3>
          {Object.entries(data.payment_breakdown).map(([k, v]) => <p key={k}>{k}: {v.toLocaleString()} đ</p>)}
        </div>
      </div>

      <div className="card" style={{ marginTop: 12 }}>
        <h3>KPI nhân sự</h3>
        <table className="table">
          <thead><tr><th>Nhân sự</th><th>Doanh thu</th><th>Lợi nhuận</th><th>Đơn</th></tr></thead>
          <tbody>
            {data.staff_kpis.map((s) => (
              <tr key={s.staff_name}><td>{s.staff_name}</td><td>{s.revenue.toLocaleString()}</td><td>{s.profit.toLocaleString()}</td><td>{s.orders}</td></tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card" style={{ marginTop: 12 }}>
        <h3>AI gợi ý</h3>
        <p>{data.ai_advice}</p>
        <small>{data.liquidity_note}</small>
      </div>
    </div>
  );
}
