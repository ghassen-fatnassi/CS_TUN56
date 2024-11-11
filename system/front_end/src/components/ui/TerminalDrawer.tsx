import * as React from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import TerminalsBox from "./TerminalsBox";
import { useDrawerContext } from "./DrawerContext";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";

export default function TerminalDrawer() {
  const { isOpen, selectedNode, closeDrawer } = useDrawerContext();

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === "Escape") {
      closeDrawer();
    }
  };

  return (
    <Drawer
      anchor="bottom"
      open={isOpen}
      onClose={closeDrawer}
      onKeyDown={handleKeyDown}
      sx={{
        "& .MuiDrawer-paper": {
          height: "auto",
          maxHeight: "90vh",
          borderTopLeftRadius: 8,
          borderTopRightRadius: 8,
          backgroundColor: "#000", // Cyber theme black
          color: "#00ff00", // Cyber green text
          boxShadow: "0 -2px 15px rgba(0, 255, 0, 0.2)",
        },
      }}
    >
      <Box
        sx={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          padding: 0,
        }}
        role="presentation"
      >
        <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 1 }}>
          <IconButton onClick={closeDrawer} aria-label="close" sx={{ color: "#00ff00" }}>
            <CloseIcon />
          </IconButton>
        </Box>

        {selectedNode && (
          <Box
            sx={{
              flexGrow: 1,
              overflowY: "auto",
              padding: 2,
              color: "#00ff00",
            }}
          >
            <Typography variant="h6" sx={{ color: "#00ff00", marginBottom: 1 }}>
              {selectedNode.name}
            </Typography>
            <Divider sx={{ borderColor: "#00ff00", marginBottom: 2 }} />

            <Box>
              <Typography variant="body2" sx={{ marginBottom: 0.5 }}>
                <strong>Type:</strong> {selectedNode.type}
              </Typography>
              <Typography variant="body2" sx={{ marginBottom: 0.5 }}>
                <strong>Status:</strong> {selectedNode.status}
              </Typography>
              <Typography variant="body2" sx={{ marginBottom: 0.5 }}>
                <strong>Activity Level:</strong> {selectedNode.rlAgentData.activityLevel}
              </Typography>
              <Typography variant="body2" sx={{ marginBottom: 0.5 }}>
                <strong>Last Action:</strong> {selectedNode.rlAgentData.lastAction}
              </Typography>
            </Box>
          </Box>
        )}

        <Box sx={{ flexGrow: 2, overflowY: "auto", padding: 2 }}>
          <TerminalsBox />
        </Box>
      </Box>
    </Drawer>
  );
}
