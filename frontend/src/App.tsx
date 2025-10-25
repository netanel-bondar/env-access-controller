import { useState, useEffect, useCallback } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Grid,
  Paper,
  Snackbar,
  Alert,
  Chip,
  CircularProgress,
} from '@mui/material';
import { Refresh as RefreshIcon } from '@mui/icons-material';
import { ResourceCard } from './components/ResourceCard';
import { apiService } from './services/api';
import type { ResourceInfo } from './types/resource';

const REFRESH_INTERVAL = 5000; // 5 seconds

function App() {
  const [username, setUsername] = useState<string>('');
  const [publishers, setPublishers] = useState<Record<string, ResourceInfo>>({});
  const [environments, setEnvironments] = useState<Record<string, ResourceInfo>>({});
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error' | 'info';
  }>({
    open: false,
    message: '',
    severity: 'info',
  });

  const showSnackbar = (message: string, severity: 'success' | 'error' | 'info') => {
    setSnackbar({ open: true, message, severity });
  };

  const fetchData = useCallback(async () => {
    try {
      const [publishersData, environmentsData] = await Promise.all([
        apiService.getAllPublishers(),
        apiService.getAllEnvironments(),
      ]);
      setPublishers(publishersData);
      setEnvironments(environmentsData);
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Error fetching data:', error);
      showSnackbar('Failed to fetch resources', 'error');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Fetch username on mount
    apiService
      .getUsername()
      .then(setUsername)
      .catch(() => setUsername('unknown'));

    // Initial fetch
    fetchData();

    // Set up polling
    const interval = setInterval(fetchData, REFRESH_INTERVAL);

    return () => clearInterval(interval);
  }, [fetchData]);

  const handleTakePublisher = async (publisherId: string) => {
    try {
      const result = await apiService.takePublisher(publisherId, username);
      showSnackbar(result.message, result.success ? 'success' : 'error');
      await fetchData();
    } catch (error) {
      showSnackbar('Failed to take publisher', 'error');
    }
  };

  const handleReleasePublisher = async (publisherId: string) => {
    try {
      const result = await apiService.releasePublisher(publisherId);
      showSnackbar(result.message, result.success ? 'success' : 'error');
      await fetchData();
    } catch (error) {
      showSnackbar('Failed to release publisher', 'error');
    }
  };

  const handleStealPublisher = async (publisherId: string) => {
    try {
      const result = await apiService.stealPublisher(publisherId, username);
      showSnackbar(result.message, 'success');
      await fetchData();
    } catch (error) {
      showSnackbar('Failed to steal publisher', 'error');
    }
  };

  const handleTakeEnvironment = async (envName: string) => {
    try {
      const result = await apiService.takeEnvironment(envName, username);
      showSnackbar(result.message, result.success ? 'success' : 'error');
      await fetchData();
    } catch (error) {
      showSnackbar('Failed to take environment', 'error');
    }
  };

  const handleReleaseEnvironment = async (envName: string) => {
    try {
      const result = await apiService.releaseEnvironment(envName);
      showSnackbar(result.message, result.success ? 'success' : 'error');
      await fetchData();
    } catch (error) {
      showSnackbar('Failed to release environment', 'error');
    }
  };

  const handleStealEnvironment = async (envName: string) => {
    try {
      const result = await apiService.stealEnvironment(envName, username);
      showSnackbar(result.message, 'success');
      await fetchData();
    } catch (error) {
      showSnackbar('Failed to steal environment', 'error');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Environment Access Controller
          </Typography>
          <Box display="flex" alignItems="center" gap={2}>
            <Chip
              label={`User: ${username}`}
              color="secondary"
              size="small"
            />
            <Chip
              icon={<RefreshIcon />}
              label={`Updated: ${lastUpdate.toLocaleTimeString()}`}
              size="small"
              variant="outlined"
              sx={{ color: 'white', borderColor: 'white' }}
            />
          </Box>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        {/* QA Publishers Section */}
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            QA Publishers
          </Typography>
          <Grid container spacing={3}>
            {Object.entries(publishers).map(([id, publisher]) => (
              <Grid item xs={12} sm={6} md={4} key={id}>
                <ResourceCard
                  id={id}
                  resource={publisher}
                  currentUser={username}
                  onTake={handleTakePublisher}
                  onRelease={handleReleasePublisher}
                  onSteal={handleStealPublisher}
                />
              </Grid>
            ))}
          </Grid>
        </Paper>

        {/* Staging Environments Section */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            Staging Environments
          </Typography>
          <Grid container spacing={3}>
            {Object.entries(environments).map(([id, env]) => (
              <Grid item xs={12} sm={6} md={4} key={id}>
                <ResourceCard
                  id={id}
                  resource={env}
                  currentUser={username}
                  onTake={handleTakeEnvironment}
                  onRelease={handleReleaseEnvironment}
                  onSteal={handleStealEnvironment}
                />
              </Grid>
            ))}
          </Grid>
        </Paper>
      </Container>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default App;
