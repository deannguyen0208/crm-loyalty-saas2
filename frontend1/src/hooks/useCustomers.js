import { useQuery } from "@tanstack/react-query";
import { getCustomers } from "../services/api";

export const useCustomers = () => {
  return useQuery({ queryKey: ["customers"], queryFn: getCustomers });
};
