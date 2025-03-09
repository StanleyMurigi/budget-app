export interface Usage {
  id: number;
  category: number;
  used_for: string;
  amount: number;
  discount: number;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  usages: Usage[];
}

export interface BudgetAllocation {
  id: number;
  category: number;
  category_name: string;
  allocated_amount: number;
}

export interface Budget {
  id: number;
  name: string;
  amount: number;
  start_date: string;
  end_date: string;
  allocations: BudgetAllocation[];
}