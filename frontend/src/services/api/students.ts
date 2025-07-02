import { api } from './config';
import type { 
  Student, 
  PaginatedResponse,
  StudentCreateRequest 
} from '../../types';

export const studentsApi = {
  getStudents: async (params?: {
    page?: number;
    size?: number;
    first_name?: string;
    last_name?: string;
    school_id?: string;
    grade_level?: string;
    is_active?: boolean;
  }): Promise<PaginatedResponse<Student>> => {
    const response = await api.get('/students/', { params });
    return response.data;
  },

  getStudent: async (id: string): Promise<Student> => {
    const response = await api.get(`/students/${id}`);
    return response.data;
  },

  createStudent: async (studentData: StudentCreateRequest): Promise<Student> => {
    const response = await api.post('/students/', studentData);
    return response.data;
  },

  updateStudent: async (id: string, studentData: Partial<StudentCreateRequest & { is_active: boolean }>): Promise<Student> => {
    const response = await api.put(`/students/${id}`, studentData);
    return response.data;
  },

  deleteStudent: async (id: string): Promise<void> => {
    await api.delete(`/students/${id}`);
  },
};
