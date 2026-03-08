import { useQuery } from "@tanstack/react-query";
import { getCampaigns } from "../services/api";

export default function Campaigns() {
  const { data } = useQuery({ queryKey: ["campaigns"], queryFn: getCampaigns });
  return (
    <div>
      <h1>Chiến dịch marketing</h1>
      <div className="grid">
        {data?.map((c) => (
          <div key={c.id} className="card">
            <h3>{c.name}</h3>
            <p>Kênh: {c.channel}</p>
            <p>Mục tiêu: {c.objective}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
