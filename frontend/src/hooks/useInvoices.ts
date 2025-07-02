import { useState, useEffect, useCallback } from 'react';
import { invoicesApi } from '../services/api';
import type { Invoice, PaginatedResponse, InvoiceCreateRequest } from '../types';

export interface UseInvoicesParams {
  page?: number;
  size?: number;
  invoice_number?: string;
  status?: string;
  amount_min?: number;
  amount_max?: number;
}

export const useInvoices = (params?: UseInvoicesParams) => {
  const [invoices, setInvoices] = useState<PaginatedResponse<Invoice> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchInvoices = useCallback(async (searchParams?: UseInvoicesParams) => {
    try {
      setLoading(true);
      setError(null);
      const data = await invoicesApi.getInvoices(searchParams || params);
      setInvoices(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch invoices');
    } finally {
      setLoading(false);
    }
  }, [params]);

  useEffect(() => {
    fetchInvoices();
  }, [fetchInvoices]);

  const createInvoice = async (invoiceData: InvoiceCreateRequest): Promise<Invoice | null> => {
    try {
      setError(null);
      const newInvoice = await invoicesApi.createInvoice(invoiceData);
      await fetchInvoices(); // Refresh the list
      return newInvoice;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create invoice');
      return null;
    }
  };

  const updateInvoice = async (id: string, invoiceData: Partial<InvoiceCreateRequest & { status: string }>): Promise<Invoice | null> => {
    try {
      setError(null);
      const updatedInvoice = await invoicesApi.updateInvoice(id, invoiceData);
      await fetchInvoices(); // Refresh the list
      return updatedInvoice;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update invoice');
      return null;
    }
  };

  const deleteInvoice = async (id: string): Promise<boolean> => {
    try {
      setError(null);
      await invoicesApi.deleteInvoice(id);
      await fetchInvoices(); // Refresh the list
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete invoice');
      return false;
    }
  };

  return {
    invoices: invoices?.items || [],
    pagination: invoices ? {
      total: invoices.total,
      page: invoices.page,
      size: invoices.size,
      pages: invoices.pages,
      has_next: invoices.has_next,
      has_previous: invoices.has_previous,
    } : null,
    loading,
    error,
    refetch: fetchInvoices,
    createInvoice,
    updateInvoice,
    deleteInvoice,
  };
};

export const useInvoice = (id: string) => {
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInvoice = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        const data = await invoicesApi.getInvoice(id);
        setInvoice(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch invoice');
      } finally {
        setLoading(false);
      }
    };

    fetchInvoice();
  }, [id]);

  return {
    invoice,
    loading,
    error,
  };
};
