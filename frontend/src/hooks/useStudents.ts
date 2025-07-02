import { useState, useEffect, useCallback } from 'react';
import { studentsApi } from '../services/api';
import type { Student, PaginatedResponse, StudentCreateRequest } from '../types';

export interface UseStudentsParams {
  page?: number;
  size?: number;
  first_name?: string;
  last_name?: string;
  school_id?: string;
  grade_level?: string;
  is_active?: boolean;
}

export const useStudents = (params?: UseStudentsParams) => {
  const [students, setStudents] = useState<PaginatedResponse<Student> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStudents = useCallback(async (searchParams?: UseStudentsParams) => {
    try {
      setLoading(true);
      setError(null);
      const data = await studentsApi.getStudents(searchParams || params);
      setStudents(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch students');
    } finally {
      setLoading(false);
    }
  }, [params]);

  useEffect(() => {
    fetchStudents();
  }, [fetchStudents]);

  const createStudent = async (studentData: StudentCreateRequest): Promise<Student | null> => {
    try {
      setError(null);
      const newStudent = await studentsApi.createStudent(studentData);
      await fetchStudents();
      return newStudent;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create student');
      return null;
    }
  };

  const updateStudent = async (id: string, studentData: Partial<StudentCreateRequest & { is_active: boolean }>): Promise<Student | null> => {
    try {
      setError(null);
      const updatedStudent = await studentsApi.updateStudent(id, studentData);
      await fetchStudents();
      return updatedStudent;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update student');
      return null;
    }
  };

  const deleteStudent = async (id: string): Promise<boolean> => {
    try {
      setError(null);
      await studentsApi.deleteStudent(id);
      await fetchStudents();
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete student');
      return false;
    }
  };

  return {
    students: students?.items || [],
    pagination: students ? {
      total: students.total,
      page: students.page,
      size: students.size,
      pages: students.pages,
      has_next: students.has_next,
      has_previous: students.has_previous,
    } : null,
    loading,
    error,
    refetch: fetchStudents,
    createStudent,
    updateStudent,
    deleteStudent,
  };
};

export const useStudent = (id: string) => {
  const [student, setStudent] = useState<Student | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStudent = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        const data = await studentsApi.getStudent(id);
        setStudent(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch student');
      } finally {
        setLoading(false);
      }
    };

    fetchStudent();
  }, [id]);

  return {
    student,
    loading,
    error,
  };
};
