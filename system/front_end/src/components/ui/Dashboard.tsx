import DeviceAlertCard from "./DeviceAlertCard";
import PageViewsBarChart from "./PageViewsBarChat";
import SessionsChart from "./SessionChart";
import StatCard, { StatCardProps } from "./StatCard";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";

// Data for StatCards
const statCardData: StatCardProps[] = [
  {
    title: "Users",
    value: "14k",
    interval: "Last 30 days",
    trend: "up",
    data: [
      200, 24, 220, 260, 240, 380, 100, 240, 280, 240, 300, 340, 320, 360, 340,
      380, 360, 400, 380, 420, 400, 640, 340, 460, 440, 480, 460, 600, 880, 920,
    ],
  },
  {
    title: "Conversions",
    value: "325",
    interval: "Last 30 days",
    trend: "down",
    data: [
      1640, 1250, 970, 1130, 1050, 900, 720, 1080, 900, 450, 920, 820, 840, 600,
      820, 780, 800, 760, 380, 740, 660, 620, 840, 500, 520, 480, 400, 360, 300,
      220,
    ],
  },
  {
    title: "Event count",
    value: "200k",
    interval: "Last 30 days",
    trend: "neutral",
    data: [
      500, 400, 510, 530, 520, 600, 530, 520, 510, 730, 520, 510, 530, 620, 510,
      530, 520, 410, 530, 520, 610, 530, 520, 610, 530, 420, 510, 430, 520, 510,
    ],
  },
];
const deviceData = [
  { name: "Firewall1", alert: "No alert" },
  { name: "Router1", alert: "Warning" },
  { name: "Server2", alert: "Critical" },
  { name: "UserHost1", alert: "No alert" },
];
export default function Dashboard() {
  return (
    <Box
      sx={{ margin: 0, width: "100%", maxWidth: { sm: "100%", md: "1700px" } }}
    >
      {/* Overview Section */}
      <Typography component="h2" variant="h6" sx={{ mb: 2 }}>
        Overview
      </Typography>
      <Grid container spacing={2} columns={12}>
        {/* StatCards */}
        {statCardData.map((card, index) => (
          <Grid key={index} size={{ xs: 12, sm: 6, lg: 3 }}>
            {/* <StatCard {...card} /> */}
            <DeviceAlertCard deviceData={deviceData} />
          </Grid>
        ))}

        {/* SessionsChart */}
        <Grid size={{ xs: 12, md: 6 }}>
          {/* <SessionsChart /> */}
          <DeviceAlertCard deviceData={deviceData} />
        </Grid>

        {/* PageViewsBarChart */}
        <Grid size={{ xs: 12, md: 6 }}>
          {/* <PageViewsBarChart /> */}
          <DeviceAlertCard deviceData={deviceData} />
        </Grid>
      </Grid>
    </Box>
  );
}
