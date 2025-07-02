import { api } from './config';
import type { 
  School, 
  PaginatedResponse,
  SchoolCreateRequest 
} from '../../types';

export const schoolsApi = {
  getSchools: async (params?: {
    page?: number;
    size?: number;
    name?: string;
    city?: string;
    is_active?: boolean;
  }): Promise<PaginatedResponse<School>> => {
    const response = await api.get('/schools/', { params });
    return response.data;
  },

  getSchool: async (id: string): Promise<School> => {
    const response = await api.get(`/schools/${id}`);
    return response.data;
  },

  createSchool: async (schoolData: SchoolCreateRequest): Promise<School> => {
    const response = await api.post('/schools/', schoolData);
    return response.data;
  },

  updateSchool: async (id: string, schoolData: Partial<SchoolCreateRequest & { is_active: boolean }>): Promise<School> => {
    const response = await api.put(`/schools/${id}`, schoolData);
    return response.data;
  },

  deleteSchool: async (id: string): Promise<void> => {
    await api.delete(`/schools/${id}`);
  },
};
