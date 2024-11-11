// src/components/ui/Alert.tsx
import React from 'react';
import { Alert as MuiAlert, AlertTitle } from '@mui/material';
import { AlertColor } from '@mui/material/Alert';
import { Error, CheckCircle, Info, Warning } from '@mui/icons-material';

interface AlertProps {
  severity?: AlertColor;
  title?: string;
  message: string;
  className?: string;
  icon?: React.ReactNode;
  onClose?: () => void;
}

export const Alert: React.FC<AlertProps> = ({
  severity = 'info',
  title,
  message,
  className,
  icon,
  onClose,
}) => {
  const getIcon = () => {
    if (icon) return icon;
    switch (severity) {
      case 'error':
        return <Error fontSize="small" />;
      case 'warning':
        return <Warning fontSize="small" />;
      case 'success':
        return <CheckCircle fontSize="small" />;
      default:
        return <Info fontSize="small" />;
    }
  };

  return (
    <MuiAlert
      severity={severity}
      className={className}
      icon={getIcon()}
      onClose={onClose ? () => onClose() : undefined}
    >
      {title && <AlertTitle>{title}</AlertTitle>}
      <AlertDescription>{message}</AlertDescription>
    </MuiAlert>
  );
};

// src/components/ui/AlertDescription.tsx
interface AlertDescriptionProps {
  children: React.ReactNode;
}

export const AlertDescription: React.FC<AlertDescriptionProps> = ({ children }) => {
  return <span>{children}</span>;
};
