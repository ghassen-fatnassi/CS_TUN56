import ThreatPostList from "./pages/blacklist";
import DashboardContainer from "./pages/dashboard";
import FileAnalyzer from "./pages/filaAnalyser";
import Graph from "./pages/graph";
import Rag from "./pages/rag";
import reactLogo from "/logo.png";
import HomeIcon from "@mui/icons-material/Home";
import InfoIcon from "@mui/icons-material/Info";
import SettingsIcon from "@mui/icons-material/Settings";
import {
  Box,
  CssBaseline,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Toolbar,
} from "@mui/material";
import { useState } from "react";
import "./App.css";

// Define the width of the drawer
const drawerWidth = 240;

function App() {
  const [page, setPage] = useState("Dashboard");

  // Function to render content based on the selected page
  const renderContent = () => {
    switch (page) {
      case "Dashboard":
        return <DashboardContainer />;
      case "Black List":
        return <ThreatPostList />;
      case "File analyzer":
        return <FileAnalyzer />;
      case "Rag":
        return <Rag />;
      case "Graph":
        return <Graph />;
      default:
        return <Typography variant="h4">Welcome</Typography>;
    }
  };

  return (
    <Box sx={{ display: "flex", width: "100vw", height: "100vh" }}>
      <CssBaseline />

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
            bgcolor: "rgb(24, 31, 36)",
            boxShadow: 3,
            color: "white",
          },
        }}
      >
        <Toolbar style={{ marginTop: "80px" }}>
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: "100%",
            }}
          >
            <img
              src={reactLogo}
              alt="Logo"
              style={{ width: 800, height: 200 }}
            />
          </Box>
        </Toolbar>
        <List>
          {["Dashboard", "Black List", "File analyzer", "Rag", "Graph"].map(
            (text, index) => (
              <ListItemButton key={text} onClick={() => setPage(text)}>
                <ListItemIcon>
                  {index === 0 ? (
                    <HomeIcon style={{ color: "white" }} />
                  ) : index === 1 ? (
                    <InfoIcon style={{ color: "white" }} />
                  ) : (
                    <SettingsIcon style={{ color: "white" }} />
                  )}
                </ListItemIcon>
                <ListItemText style={{ color: "white" }} primary={text} />
              </ListItemButton>
            )
          )}
        </List>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: "100%",
          height: "100vh",
          bgcolor: "rgb(24, 31, 36)",
          overflow: "auto",
        }}
      >
        {renderContent()}
      </Box>
    </Box>
  );
}

export default App;
