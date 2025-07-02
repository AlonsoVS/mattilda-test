import { api } from './config';
import type { 
  Invoice, 
  PaginatedResponse,
  InvoiceCreateRequest 
} from '../../types';

export const invoicesApi = {
  getInvoices: async (params?: {
    page?: number;
    size?: number;
    school_id?: string;
    status?: string;
    amount_min?: number;
    amount_max?: number;
  }): Promise<PaginatedResponse<Invoice>> => {
    const response = await api.get('/invoices/', { params });
    return response.data;
  },

  getInvoice: async (id: string): Promise<Invoice> => {
    const response = await api.get(`/invoices/${id}`);
    return response.data;
  },

  createInvoice: async (invoiceData: InvoiceCreateRequest): Promise<Invoice> => {
    const response = await api.post('/invoices/', invoiceData);
    return response.data;
  },

  updateInvoice: async (id: string, invoiceData: Partial<InvoiceCreateRequest & { status: string }>): Promise<Invoice> => {
    const response = await api.put(`/invoices/${id}`, invoiceData);
    return response.data;
  },

  deleteInvoice: async (id: string): Promise<void> => {
    await api.delete(`/invoices/${id}`);
  },
};
