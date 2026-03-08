import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createCustomer } from "../services/api";
import { useState } from "react";
import CustomerModal from "../components/CustomerModal";
import { useCustomers } from "../hooks/useCustomers";

export default function Customers() {
  const [modalOpen, setModalOpen] = useState(false);
  const queryClient = useQueryClient();
  const { data: customers, isLoading } = useCustomers();

  const createMutation = useMutation({
    mutationFn: createCustomer,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customers"] });
      setModalOpen(false);
    },
  });

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h1>Khách hàng</h1>
        <button className="btn primary" onClick={() => setModalOpen(true)}>Thêm khách</button>
      </div>
      {isLoading ? <p>Đang tải...</p> : (
        <div className="grid">
          {customers?.map((c) => (
            <div key={c.id} className="card">
              <b>{c.name}</b>
              <p>{c.phone}</p>
              <p>Segment: {c.segment}</p>
              <p>Điểm: {c.loyalty_points}</p>
            </div>
          ))}
        </div>
      )}
      <CustomerModal isOpen={modalOpen} onClose={() => setModalOpen(false)} onSubmit={createMutation.mutate} />
    </div>
  );
}
