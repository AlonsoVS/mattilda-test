import { useState, useEffect, useCallback } from 'react';
import { schoolsApi } from '../services/api';
import type { School, PaginatedResponse, SchoolCreateRequest } from '../types';

export interface UseSchoolsParams {
  page?: number;
  size?: number;
  name?: string;
  city?: string;
  is_active?: boolean;
}

export const useSchools = (params?: UseSchoolsParams) => {
  const [schools, setSchools] = useState<PaginatedResponse<School> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSchools = useCallback(async (searchParams?: UseSchoolsParams) => {
    try {
      setLoading(true);
      setError(null);
      const data = await schoolsApi.getSchools(searchParams || params);
      setSchools(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch schools');
    } finally {
      setLoading(false);
    }
  }, [params]);

  useEffect(() => {
    fetchSchools();
  }, [fetchSchools]);

  const createSchool = async (schoolData: SchoolCreateRequest): Promise<School | null> => {
    try {
      setError(null);
      const newSchool = await schoolsApi.createSchool(schoolData);
      await fetchSchools(); // Refresh the list
      return newSchool;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create school');
      return null;
    }
  };

  const updateSchool = async (id: string, schoolData: Partial<SchoolCreateRequest & { is_active: boolean }>): Promise<School | null> => {
    try {
      setError(null);
      const updatedSchool = await schoolsApi.updateSchool(id, schoolData);
      await fetchSchools(); // Refresh the list
      return updatedSchool;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update school');
      return null;
    }
  };

  const deleteSchool = async (id: string): Promise<boolean> => {
    try {
      setError(null);
      await schoolsApi.deleteSchool(id);
      await fetchSchools(); // Refresh the list
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete school');
      return false;
    }
  };

  return {
    schools: schools?.items || [],
    pagination: schools ? {
      total: schools.total,
      page: schools.page,
      size: schools.size,
      pages: schools.pages,
      has_next: schools.has_next,
      has_previous: schools.has_previous,
    } : null,
    loading,
    error,
    refetch: fetchSchools,
    createSchool,
    updateSchool,
    deleteSchool,
  };
};

export const useSchool = (id: string) => {
  const [school, setSchool] = useState<School | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSchool = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        const data = await schoolsApi.getSchool(id);
        setSchool(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch school');
      } finally {
        setLoading(false);
      }
    };

    fetchSchool();
  }, [id]);

  return {
    school,
    loading,
    error,
  };
};
