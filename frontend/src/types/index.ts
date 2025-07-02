// API Response Types
export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface School {
  id: string;
  name: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  phone: string;
  email: string;
  principal: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Student {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  date_of_birth: string;
  grade_level: string;
  school_id: string;
  school?: School;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Invoice {
  id: string;
  invoice_number: string;
  school_id: string;
  school?: School;
  amount: number;
  due_date: string;
  status: 'pending' | 'paid' | 'overdue' | 'cancelled';
  description: string;
  created_at: string;
  updated_at: string;
}

// Request Types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserCreateRequest {
  email: string;
  name: string;
  password: string;
  role?: string;
}

export interface SchoolCreateRequest {
  name: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  phone: string;
  email: string;
  principal: string;
}

export interface StudentCreateRequest {
  first_name: string;
  last_name: string;
  email: string;
  date_of_birth: string;
  grade_level: string;
  school_id: string;
}

export interface InvoiceCreateRequest {
  school_id: string;
  amount: number;
  due_date: string;
  description: string;
}

// Pagination Types
export interface PaginationParams {
  page: number;
  size: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
  has_next?: boolean;
  has_previous?: boolean;
}

// Dashboard Stats
export interface DashboardStats {
  total_users: number;
  total_schools: number;
  total_students: number;
  total_invoices: number;
  pending_invoices: number;
  overdue_invoices: number;
}