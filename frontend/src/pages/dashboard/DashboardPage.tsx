import { Typography, Paper, Box, Grid, CircularProgress } from '@mui/material';
import { School, Person, Receipt, TrendingUp, CheckCircle, AccessTime } from '@mui/icons-material';
import { useDashboard } from '../../hooks';

const DashboardPage = () => {
  const { stats, loading, error } = useDashboard();

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Typography color="error">
          Failed to load dashboard data: {error}
        </Typography>
      </Box>
    );
  }

  const dashboardStats = [
    { 
      title: 'Total Schools', 
      value: stats?.total_schools?.toString() || '0', 
      icon: <School />, 
      color: '#388e3c' 
    },
    { 
      title: 'Active Schools', 
      value: stats?.active_schools?.toString() || '0', 
      icon: <CheckCircle />, 
      color: '#2e7d32' 
    },
    { 
      title: 'Total Students', 
      value: stats?.total_students?.toString() || '0', 
      icon: <Person />, 
      color: '#f57c00' 
    },
    { 
      title: 'Active Students', 
      value: stats?.active_students?.toString() || '0', 
      icon: <Person />, 
      color: '#ff8f00' 
    },
    { 
      title: 'Total Invoices', 
      value: stats?.total_invoices?.toString() || '0', 
      icon: <Receipt />, 
      color: '#d32f2f' 
    },
    { 
      title: 'Pending Invoices', 
      value: stats?.pending_invoices?.toString() || '0', 
      icon: <AccessTime />, 
      color: '#f44336' 
    },
    { 
      title: 'Total Revenue', 
      value: `$${stats?.total_revenue?.toLocaleString() || '0'}`, 
      icon: <TrendingUp />, 
      color: '#1976d2' 
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {dashboardStats.map((stat) => (
          <Grid key={stat.title} size={{ xs: 12, sm: 6, md: 4, lg: 3 }}>
            <Paper
              sx={{
                p: 3,
                display: 'flex',
                alignItems: 'center',
                gap: 2,
                borderLeft: `4px solid ${stat.color}`,
                minHeight: '120px',
              }}
            >
              <Box sx={{ color: stat.color, fontSize: '2rem' }}>{stat.icon}</Box>
              <Box>
                <Typography variant="h5" sx={{ fontWeight: 'bold', color: stat.color }}>
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.title}
                </Typography>
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Welcome to School Management System
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Use the navigation menu to explore the different sections:
          </Typography>
          <Box component="ul" sx={{ mt: 2 }}>
            <li>
              <Typography variant="body2">
                <strong>Users:</strong> Manage system users and administrators
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                <strong>Schools:</strong> Add and manage school information
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                <strong>Students:</strong> Student registration and profiles
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                <strong>Invoices:</strong> Billing and payment management
              </Typography>
            </li>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};

export default DashboardPage;
