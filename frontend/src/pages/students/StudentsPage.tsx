import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  TextField,
  Chip,
  CircularProgress,
  Alert,
  Pagination,
} from '@mui/material';
import { Add, Search } from '@mui/icons-material';
import { useStudents } from '../../hooks';
import type { Student } from '../../types';

const StudentsPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const { 
    students, 
    loading, 
    error, 
    pagination,
    refetch,
    createStudent,
    updateStudent,
    deleteStudent 
  } = useStudents();

  useEffect(() => {
    refetch({ page, first_name: searchTerm });
  }, [page, searchTerm, refetch]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setPage(1); // Reset to first page when searching
  };

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  if (loading && students.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Students</Typography>
        <Button variant="contained" startIcon={<Add />}>
          Add Student
        </Button>
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search students..."
          value={searchTerm}
          onChange={handleSearch}
          InputProps={{
            startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />,
          }}
        />
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>School</TableCell>
              <TableCell>Grade</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {students.map((student: Student) => (
              <TableRow key={student.id}>
                <TableCell>{`${student.first_name} ${student.last_name}`}</TableCell>
                <TableCell>{student.email}</TableCell>
                <TableCell>{student.school_id}</TableCell>
                <TableCell>
                  <Chip label={student.grade_level} size="small" />
                </TableCell>
                <TableCell>
                  <Chip
                    label={student.is_active ? 'Active' : 'Inactive'}
                    size="small"
                    color={student.is_active ? 'success' : 'default'}
                  />
                </TableCell>
                <TableCell>
                  <Button size="small" sx={{ mr: 1 }}>
                    Edit
                  </Button>
                  <Button 
                    size="small" 
                    color="error"
                    onClick={() => deleteStudent(student.id)}
                  >
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {pagination && pagination.pages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <Pagination
            count={pagination.pages}
            page={page}
            onChange={handlePageChange}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
};

export default StudentsPage;
