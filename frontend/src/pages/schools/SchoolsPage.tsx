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
import { useSchools } from '../../hooks';
import type { School } from '../../types';

const SchoolsPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const { 
    schools, 
    loading, 
    error, 
    pagination,
    refetch,
    createSchool,
    updateSchool,
    deleteSchool 
  } = useSchools();

  useEffect(() => {
    refetch({ page, name: searchTerm });
  }, [page, searchTerm, refetch]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setPage(1); // Reset to first page when searching
  };

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  if (loading && schools.length === 0) {
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
        <Typography variant="h4">Schools</Typography>
        <Button variant="contained" startIcon={<Add />}>
          Add School
        </Button>
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search schools..."
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
              <TableCell>Address</TableCell>
              <TableCell>City</TableCell>
              <TableCell>Phone</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Principal</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {schools.map((school: School) => (
              <TableRow key={school.id}>
                <TableCell>{school.name}</TableCell>
                <TableCell>{school.address}</TableCell>
                <TableCell>{school.city}</TableCell>
                <TableCell>{school.phone}</TableCell>
                <TableCell>{school.email}</TableCell>
                <TableCell>{school.principal}</TableCell>
                <TableCell>
                  <Chip
                    label={school.is_active ? 'Active' : 'Inactive'}
                    size="small"
                    color={school.is_active ? 'success' : 'default'}
                  />
                </TableCell>
                <TableCell>
                  <Button size="small" sx={{ mr: 1 }}>
                    Edit
                  </Button>
                  <Button 
                    size="small" 
                    color="error"
                    onClick={() => deleteSchool(school.id)}
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

export default SchoolsPage;
