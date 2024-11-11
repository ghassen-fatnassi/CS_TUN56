import {
  Card,
  CardContent,
  CardHeader,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Box,
} from "@mui/material";
import React from "react";

// Define the types for device data
interface Device {
  name: string;
  alert: string;
}

interface DeviceAlertCardProps {
  deviceData: Device[];
}

const DeviceAlertCard: React.FC<DeviceAlertCardProps> = ({ deviceData }) => {
  return (
    <Card
      variant="outlined"
      sx={{
        backgroundColor: "#131a22",
        border: "1px solid #30c48b",
        borderRadius: "12px",
        boxShadow: "0 0 10px rgba(0, 255, 0, 0.5)",
      }}
    >
      <CardHeader
        title={<Typography variant="h6">Device Alerts</Typography>}
        sx={{
          backgroundColor: "#131a22",
          color: "#30c48b",
        }}
      />
      <CardContent>
        <TableContainer component={Box}>
          <Table size="small" aria-label="Device Alerts Table">
            <TableHead>
              <TableRow>
                <TableCell sx={{ color: "#30c48b", fontWeight: "bold" }}>
                  Device Name
                </TableCell>
                <TableCell sx={{ color: "#30c48b", fontWeight: "bold" }}>
                  Alert Status
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {deviceData.map((device, index) => (
                <TableRow key={index}>
                  <TableCell sx={{ color: "white" }}>{device.name}</TableCell>
                  <TableCell
                    sx={{
                      color:
                        device.alert === "Critical"
                          ? "#f44336"
                          : device.alert === "Warning"
                          ? "#ff9800"
                          : "#4caf50",
                    }}
                  >
                    {device.alert}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </CardContent>
    </Card>
  );
};

export default DeviceAlertCard;
