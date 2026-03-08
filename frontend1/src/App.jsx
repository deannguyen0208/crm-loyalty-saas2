import { useEffect, useState } from 'react';
import { api } from './services/api';

const formatMoney = (v) => new Intl.NumberFormat('vi-VN').format(Math.round(v || 0));

function App() {
  const [period, setPeriod] = useState('month');
  const [summary, setSummary] = useState(null);
  const [bestSeller, setBestSeller] = useState([]);
  const [kpi, setKpi] = useState([]);
  const [advice, setAdvice] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        setError('');
        const [s, b, k, a] = await Promise.all([
          api(`/analytics/summary?period=${period}`),
          api('/analytics/best-sellers'),
          api('/analytics/employee-kpi'),
          api('/ai/advice'),
        ]);
        setSummary(s);
        setBestSeller(b);
        setKpi(k);
        setAdvice(a);
      } catch (e) {
        setError('Không tải được dữ liệu, hãy chạy backend ở cổng 8000.');
      }
    }
    load();
  }, [period]);

  return (
    <div className="page">
      <header className="hero">
        <h1>Cafe SaaS cho quán nhỏ ~100m²</h1>
        <p>Quản lý doanh thu, lợi nhuận, KPI nhân sự, best-seller, và tư vấn AI.</p>
      </header>
      {error && <p className="error">{error}</p>}
      <section className="controls">
        <label>Chu kỳ phân tích:</label>
        <select value={period} onChange={(e) => setPeriod(e.target.value)}>
          <option value="week">Tuần</option>
          <option value="month">Tháng</option>
          <option value="quarter">Quý</option>
          <option value="year">Năm</option>
        </select>
      </section>

      {summary && (
        <section className="grid">
          <article className="card"><h3>Doanh thu</h3><strong>{formatMoney(summary.revenue)} đ</strong></article>
          <article className="card"><h3>Lợi nhuận</h3><strong>{formatMoney(summary.profit)} đ</strong></article>
          <article className="card"><h3>Biên lợi nhuận</h3><strong>{summary.margin}%</strong></article>
          <article className="card"><h3>Số đơn</h3><strong>{summary.order_count}</strong></article>
        </section>
      )}

      <section className="two-col">
        <article className="card">
          <h3>Top best-seller</h3>
          <ul>
            {bestSeller.map((item) => (
              <li key={item.product}>{item.product} — {item.quantity} ly</li>
            ))}
          </ul>
        </article>
        <article className="card">
          <h3>KPI nhân sự</h3>
          <ul>
            {kpi.map((item) => (
              <li key={item.employee}>{item.employee}: {formatMoney(item.revenue)} đ ({item.completion}%)</li>
            ))}
          </ul>
        </article>
      </section>

      {advice && (
        <section className="card advice">
          <h3>Khuyến nghị AI</h3>
          <p>{advice.insight}</p>
          <small>Gợi ý quyết định: {advice.decision_hint}</small>
        </section>
      )}
    </div>
  );
}

export default App;
