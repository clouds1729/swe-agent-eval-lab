import { useEffect, useMemo, useState } from "react";

export type Transaction = {
  id: string;
  employee: string;
  merchant: string;
  amount: number;
  approved: boolean;
};

const seedTransactions: Transaction[] = [
  { id: "t1", employee: "Alice", merchant: "Paper Co", amount: 42, approved: false },
  { id: "t2", employee: "Alice", merchant: "Travel Hub", amount: 120, approved: false },
  { id: "t3", employee: "Bob", merchant: "Cafe 9", amount: 16, approved: true }
];

export function App() {
  const [transactions] = useState<Transaction[]>(seedTransactions);
  const [selectedEmployee, setSelectedEmployee] = useState<string>("All");

  const filtered = useMemo(() => {
    if (selectedEmployee === "All") return transactions;
    return transactions.filter((t) => t.employee === selectedEmployee);
  }, [selectedEmployee, transactions]);

  // BUG: approval edits are applied only to this transient view state.
  const [approvalOverrides, setApprovalOverrides] = useState<Record<string, boolean>>({});

  useEffect(() => {
    setApprovalOverrides({});
  }, [selectedEmployee]);

  const visibleRows = filtered.map((tx) => ({
    ...tx,
    approved: approvalOverrides[tx.id] ?? tx.approved
  }));

  const toggleApproval = (id: string) => {
    const tx = filtered.find((row) => row.id === id);
    if (!tx) return;

    setApprovalOverrides((prev) => ({
      ...prev,
      [id]: !(prev[id] ?? tx.approved)
    }));
  };

  return (
    <div>
      <h1>Transaction approvals</h1>
      <label htmlFor="employee-filter">Employee</label>{" "}
      <select
        id="employee-filter"
        aria-label="Employee"
        value={selectedEmployee}
        onChange={(e) => setSelectedEmployee(e.target.value)}
      >
        <option>All</option>
        <option>Alice</option>
        <option>Bob</option>
      </select>

      <ul>
        {visibleRows.map((tx) => (
          <li key={tx.id}>
            <span>{tx.employee}</span> - <span>{tx.merchant}</span> - <span>${tx.amount}</span>{" "}
            <label>
              Approved
              <input
                type="checkbox"
                aria-label={`approve-${tx.id}`}
                checked={tx.approved}
                onChange={() => toggleApproval(tx.id)}
              />
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}
