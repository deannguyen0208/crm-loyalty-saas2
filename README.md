# Cafe SaaS (MVP)

Nền tảng SaaS tối ưu cho chủ quán cafe nhỏ (~100m2) với các nhóm chức năng chính:

- Đăng ký/đăng nhập bằng email hoặc số điện thoại + mật khẩu mạnh.
- Theo dõi doanh thu/lợi nhuận theo tuần, tháng, quý, năm.
- Phân tích top sản phẩm bán chạy (best seller).
- Phân tích KPI nhân sự theo target doanh thu.
- Ghi nhận thanh toán qua MOMO, ZaloPay, chuyển khoản ngân hàng, tiền mặt.
- Tư vấn AI (rule-based) dựa trên dữ liệu vận hành.
- Snapshot dữ liệu lên thư mục cloud backup.
- Export báo cáo JSON để đảm bảo tính thanh khoản dữ liệu khi ngừng sử dụng.

## Backend

```bash
cd backend
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend1
npm install
npm run dev
```

> Nếu môi trường chặn npm registry, frontend sẽ không cài dependency được và cần mirror nội bộ.

## Khuyến nghị bảo mật production

- Đưa DB sang PostgreSQL managed cloud.
- Dùng object storage (S3/R2/GCS) cho snapshot/export.
- Bật WAF + rate limit + bot protection.
- Kết nối đơn vị pentest/SOC để giám sát gian lận.
- Bật MFA, xác thực thiết bị, và nhật ký audit bất biến.
