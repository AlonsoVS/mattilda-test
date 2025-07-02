import { schoolsApi } from './schools';
import { studentsApi } from './students';
import { invoicesApi } from './invoices';

export interface DashboardStats {
  total_schools: number;
  total_students: number;
  total_invoices: number;
  active_schools: number;
  active_students: number;
  pending_invoices: number;
  total_revenue: number;
}

export const dashboardApi = {
  getStats: async (): Promise<DashboardStats> => {
    const [schools, students, invoices, activeSchools, activeStudents, pendingInvoices] = await Promise.all([
      schoolsApi.getSchools({ page: 1, size: 1 }),
      studentsApi.getStudents({ page: 1, size: 1 }),
      invoicesApi.getInvoices({ page: 1, size: 1 }),
      schoolsApi.getSchools({ page: 1, size: 1, is_active: true }),
      studentsApi.getStudents({ page: 1, size: 1, is_active: true }),
      invoicesApi.getInvoices({ page: 1, size: 1, status: 'pending' }),
    ]);

    // Calculate total revenue from all paid invoices
    const paidInvoices = await invoicesApi.getInvoices({ page: 1, size: 100, status: 'paid' });
    const totalRevenue = paidInvoices.items?.reduce((sum, invoice) => sum + (invoice.amount || 0), 0) || 0;

    return {
      total_schools: schools.total || 0,
      total_students: students.total || 0,
      total_invoices: invoices.total || 0,
      active_schools: activeSchools.total || 0,
      active_students: activeStudents.total || 0,
      pending_invoices: pendingInvoices.total || 0,
      total_revenue: totalRevenue,
    };
  },
};
