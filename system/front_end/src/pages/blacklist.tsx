import DeleteIcon from "@mui/icons-material/Delete";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Card,
  CardContent,
  Box,
  Tooltip,
  Alert,
  AlertTitle,
} from "@mui/material";
import { Shield, User, AlertTriangle, Ban, CheckCircle } from "lucide-react";
import React, { useState, useEffect } from "react";

interface Post {
  id: string;
  name: string;
  text: string;
  threatLevel: 1 | 2 | 3 | 4;
  creatorId: string;
}

const ThreatPostList: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [_, setBlacklistModalOpen] = useState(false);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const requestBody = {
        classifier_mode: "severity",
        window_size_list: [2, 3, 4],
        ngram_extract_mode: "all",
        eval_data: [
          {
            text: 'rt engadget " <TARGET> man gets 00 months in prison for emergency system ddos attacks https:t.co0pqrpdixsu "',
          },
          {
            text: "<TARGET> android on qualcomm secure app pointer dereference memory corruption : a vulnerability was found in google https:t.cogkzaixkoyg",
          },
          {
            text: "this is a rare moment of vulnerability for me , but sometimes i deeply fear that there will be an <TARGET> update that https:t.coikox0ccqzb",
          },
          {
            text: "<TARGET> addresses #spectre #security vulnerability previously identified by google researchers with the release o https:t.cofkymdb0fkl",
          },
          {
            text: "@survivetheark server 000 on <TARGET> has been being ddos'd for a while now 😢😓😭",
          },
        ],
      };

      console.log("Attempting to fetch posts...");
      const response = await fetch(
        "https://7528-196-203-181-122.ngrok-free.app/evaluate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        }
      );

      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("Data fetched successfully:", data);

      // Assuming response has an array of probabilities and texts, like
      // data.evaluation_results = [{ text: "sample text", probability: 0.85 }, ...]
      const evaluationResults = data.evaluation_results.map((result: any) => {
        const threatLevel = determineThreatLevel(result.severity_prob);
        return {
          id: generateUniqueId(), // Assuming a unique ID generation method
          name: "User", // Placeholder or fetched name
          text: result.text,
          threatLevel: threatLevel,
          creatorId: generateUniqueCreatorId(), // Placeholder or fetched creator ID
        };
      });

      setPosts(evaluationResults);
    } catch (error) {
      console.error("Error fetching posts:", error);
    }
  };

  // Helper function to determine threat level based on probability
  const determineThreatLevel = (probability: number): 1 | 2 | 3 | 4 => {
    if (probability < 0.05) {
      return 1; // Low Threat
    } else if (probability < 0.15) {
      return 2; // Moderate Threat
    } else if (probability < 0.3) {
      return 3; // High Threat
    } else {
      return 4; // Critical Threat
    }
  };

  // Utility function to generate unique IDs (e.g., UUID)
  const generateUniqueId = (): string => {
    return Math.random().toString(36).substr(2, 9);
  };

  const generateUniqueCreatorId = (): string => {
    return Math.random().toString(36).substr(2, 9);
  };

  const handleRemoveFromBlacklist = (creatorId: string) => {
    const updatedPosts = posts.filter((post) => post.creatorId !== creatorId);
    setPosts(updatedPosts);
  };

  const handleOpenBlacklistModal = () => {
    setBlacklistModalOpen(true);
  };

  const getThreatLevelInfo = (level: 1 | 2 | 3 | 4) => {
    const levels = {
      1: { label: "Low", color: "#4caf50", icon: CheckCircle },
      2: { label: "Moderate", color: "#ff9800", icon: Shield },
      3: { label: "High", color: "#fb8c00", icon: AlertTriangle },
      4: { label: "Critical", color: "#f44336", icon: Ban },
    };
    return levels[level] || levels[1];
  };

  return (
    <Box
      sx={{ minHeight: "100vh", bgcolor: "rgb(24, 31, 36)", marginTop: "8rem" }}
    >
      <AppBar position="fixed">
        <Toolbar
          sx={{ bgcolor: "rgb(24, 31, 36)", boxShadow: 3, height: "6rem" }}
        >
          <Typography
            variant="h6"
            component="div"
            sx={{
              flexGrow: 1,
              textAlign: "center",
              bgcolor: "rgb(24, 31, 36)",
              color: "#30c48b",
            }}
          >
            Threat Posts
          </Typography>
        </Toolbar>
      </AppBar>

      <Box
        sx={{
          maxWidth: "1200px",
          mx: "auto",
          p: 3,
          // mt: 10,
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mb: 4,
          }}
        >
          <Typography variant="h5" color="white">
            Blacklisted Users' Tweets
          </Typography>
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 2,
            }}
          >
            <Alert
              severity="info"
              sx={{
                display: "flex",
                alignItems: "center",
                bgcolor: "transparent",
              }}
            >
              <AlertTitle style={{ color: "#6e7276" }}>Info</AlertTitle>
              <strong style={{ color: "white" }}>{posts.length}</strong>{" "}
              <span style={{ color: "white" }}>blacklisted posts</span>
            </Alert>
            <Button
              variant="contained"
              color="primary"
              onClick={handleOpenBlacklistModal}
              style={{ backgroundColor: "transparent", border: "none" }}
            >
              Manage Blacklist
            </Button>
          </Box>
        </Box>

        <Box sx={{ display: "grid", gap: 3 }}>
          {posts.length === 0 ? (
            <Typography variant="body1" color="aliceblue">
              No blacklisted posts to display.
            </Typography>
          ) : (
            posts.map((post) => {
              const threatInfo = getThreatLevelInfo(post.threatLevel);
              const ThreatIcon = threatInfo.icon;

              return (
                <Card
                  key={post.id}
                  variant="outlined"
                  sx={{
                    borderLeft: `4px solid`,
                    borderColor: threatInfo.color,
                    transition: "box-shadow 0.3s",
                    "&:hover": {
                      boxShadow: 6,
                    },
                  }}
                  style={{ backgroundColor: "rgb(27, 37, 46)" }}
                >
                  <CardContent>
                    <Box
                      sx={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "flex-start",
                      }}
                    >
                      <Box
                        sx={{ display: "flex", alignItems: "center", gap: 2 }}
                      >
                        <Box
                          sx={{
                            bgcolor: "#131a22",
                            p: 1.5,
                            borderRadius: "50%",
                          }}
                        >
                          <User size={24} color={threatInfo.color} />
                        </Box>
                        <Box>
                          <Box
                            sx={{
                              display: "flex",
                              alignItems: "center",
                              gap: 1,
                              mt: 0.5,
                              bgColor: "#131a22",
                            }}
                          >
                            <ThreatIcon color={threatInfo.color} size={18} />
                            <Typography variant="body2" color="text.primary">
                              {threatInfo.label} Threat Level
                            </Typography>
                          </Box>
                        </Box>
                      </Box>
                      <Tooltip title="Delete tweet">
                        <IconButton
                          color="error"
                          onClick={() =>
                            handleRemoveFromBlacklist(post.creatorId)
                          }
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </Box>

                    <Box
                      sx={{ mt: 2, p: 2, bgcolor: "#131a22", borderRadius: 1 }}
                    >
                      <Typography variant="body1" color="white">
                        {post.text}
                      </Typography>
                    </Box>

                    <Box
                      sx={{
                        mt: 2,
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                      }}
                    >
                      <Typography variant="caption" color="text.secondary">
                        User ID: {post.creatorId}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              );
            })
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default ThreatPostList;
