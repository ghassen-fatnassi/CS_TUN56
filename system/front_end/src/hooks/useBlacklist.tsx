import { useState, useEffect } from 'react';
import axios from 'axios';

interface BlacklistState {
  blacklist: string[];
  addToBlacklist: (userId: string) => void;
  removeFromBlacklist: (userId: string) => void;
}

const useBlacklist = (): BlacklistState => {
  const [blacklist, setBlacklist] = useState<string[]>([]);

  useEffect(() => {
    // Fetch the blacklist from the server on component mount
    const fetchBlacklist = async () => {
      try {
        // Use mock data for debugging
        const mockBlacklist = ['user1', 'user2', 'user3'];
        setBlacklist(mockBlacklist);
      } catch (error) {
        console.error('Error fetching blacklist:', error);
      }
    };
    fetchBlacklist();
  }, []);

  const addToBlacklist = async (userId: string) => {
    try {
      // Update the mock blacklist
      setBlacklist((prevBlacklist) => [...prevBlacklist, userId]);
    } catch (error) {
      console.error('Error adding to blacklist:', error);
    }
  };

  const removeFromBlacklist = async (userId: string) => {
    try {
      // Update the mock blacklist
      setBlacklist((prevBlacklist) => prevBlacklist.filter((id) => id !== userId));
    } catch (error) {
      console.error('Error removing from blacklist:', error);
    }
  };

  return { blacklist, addToBlacklist, removeFromBlacklist };
};

export default useBlacklist;