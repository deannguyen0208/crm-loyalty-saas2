import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getCustomers, createCustomer } from "../services/api";
import { useState } from "react";
import CustomerModal from "../components/CustomerModal";

export default function Customers() {
  const [modalOpen, setModalOpen] = useState(false);
  const queryClient = useQueryClient();

  const { data: customers, isLoading } = useQuery({
    queryKey: ["customers"],
    queryFn: getCustomers,
  });

  const createMutation = useMutation({
    mutationFn: createCustomer,
    onSuccess: () => {
      queryClient.invalidateQueries(["customers"]);
      setModalOpen(false);
    },
  });

  return (
    <div className="p-4">
      <div className="flex justify-between mb-4">
        <h1 className="text-2xl font-bold">Khách hàng</h1>
        <button
          onClick={() => setModalOpen(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Thêm khách
        </button>
      </div>
      {isLoading ? (
        <div>Đang tải...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {customers?.map((c) => (
            <div key={c.id} className="border p-4 rounded shadow">
              <div className="font-bold">{c.name}</div>
              <div>{c.phone}</div>
              <div>Điểm: {c.points}</div>
              <div className="flex gap-2 mt-2">
                {c.tags.map((tag) => (
                  <span
                    key={tag}
                    className="bg-gray-200 px-2 py-1 rounded text-sm"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
      <CustomerModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={createMutation.mutate}
      />
    </div>
  );
}
