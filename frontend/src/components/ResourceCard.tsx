import { useState } from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Switch,
  Button,
  Chip,
  Box,
  CircularProgress,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  PersonOff as StealIcon,
} from '@mui/icons-material';
import type { ResourceInfo } from '../types/resource';

interface ResourceCardProps {
  id: string;
  resource: ResourceInfo;
  currentUser: string;
  onTake: (id: string) => Promise<void>;
  onRelease: (id: string) => Promise<void>;
  onSteal: (id: string) => Promise<void>;
}

export const ResourceCard = ({
  id,
  resource,
  currentUser,
  onTake,
  onRelease,
  onSteal,
}: ResourceCardProps) => {
  const [loading, setLoading] = useState(false);

  const hasUsername = currentUser && currentUser.trim().length > 0;
  const isTakenByCurrentUser = resource.is_taken && resource.taken_by === currentUser;
  const isTakenByOther = resource.is_taken && resource.taken_by !== currentUser;

  const handleToggle = async () => {
    setLoading(true);
    try {
      if (isTakenByCurrentUser) {
        await onRelease(id);
      } else if (!resource.is_taken) {
        await onTake(id);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSteal = async () => {
    setLoading(true);
    try {
      await onSteal(id);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      sx={{
        minWidth: 275,
        opacity: loading ? 0.6 : 1,
        transition: 'opacity 0.3s',
        border: isTakenByCurrentUser ? '2px solid #4caf50' : 'none',
      }}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="h6" component="div">
            {resource.name}
          </Typography>
          {resource.is_taken ? (
            <Chip
              icon={isTakenByCurrentUser ? <CheckCircleIcon /> : <CancelIcon />}
              label={isTakenByCurrentUser ? 'Taken by you' : 'Taken'}
              color={isTakenByCurrentUser ? 'success' : 'error'}
              size="small"
            />
          ) : (
            <Chip label="Available" color="default" size="small" />
          )}
        </Box>

        {resource.is_taken && (
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Owned by: <strong>{resource.taken_by}</strong>
          </Typography>
        )}

        {resource.is_taken && resource.taken_at && (
          <Typography variant="caption" color="text.secondary">
            Since: {new Date(resource.taken_at).toLocaleString()}
          </Typography>
        )}

        {resource.metadata && Object.keys(resource.metadata).length > 0 && (
          <Box mt={2}>
            {Object.entries(resource.metadata).map(([key, value]) => (
              <Typography key={key} variant="caption" display="block" color="text.secondary">
                {key}: {String(value)}
              </Typography>
            ))}
          </Box>
        )}
      </CardContent>

      <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
        <Box display="flex" alignItems="center">
          <Typography variant="body2" sx={{ mr: 1 }}>
            {isTakenByCurrentUser ? 'Release' : 'Take'}
          </Typography>
          <Switch
            checked={isTakenByCurrentUser}
            onChange={handleToggle}
            disabled={loading || isTakenByOther || !hasUsername}
            color="success"
          />
        </Box>

        {isTakenByOther && (
          <Button
            variant="outlined"
            color="warning"
            size="small"
            startIcon={loading ? <CircularProgress size={16} /> : <StealIcon />}
            onClick={handleSteal}
            disabled={loading || !hasUsername}
          >
            Steal
          </Button>
        )}
      </CardActions>
    </Card>
  );
};
