import * as d3 from "d3";
import React, { createContext, useContext, useState } from "react";

// Define types for node data and context
interface NodeData {
  id: string;
  name: string;
  type: string;
  status: string;
  rlAgentData: {
    activityLevel: number;
    lastAction: string;
  };
}

interface ActionData {
  blue_action: string;
  host_blue: string;
  red_action: string;
  host_red: string;
}

interface DrawerContextType {
  isOpen: boolean;
  selectedNode: NodeData | null;
  attackerAction: string | null;
  defenderAction: string | null;
  openDrawer: (node: NodeData) => void;
  closeDrawer: () => void;
}

// Initialize the context
const DrawerContext = createContext<DrawerContextType | undefined>(undefined);

// Provide the context to the components
export const DrawerProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedNode, setSelectedNode] = useState<NodeData | null>(null);
  const [attackerAction, setAttackerAction] = useState<string | null>(null);
  const [defenderAction, setDefenderAction] = useState<string | null>(null);

  const openDrawer = async (node: NodeData) => {
    setSelectedNode(node);
    setIsOpen(true);
    await fetchActions(node.id);
  };

  const closeDrawer = () => {
    setIsOpen(false);
    setSelectedNode(null);
    setAttackerAction(null);
    setDefenderAction(null);
  };

  const fetchActions = async (nodeId: string) => {
    try {
      const data = (await d3.csv("/actions_list.csv")) as ActionData[];
      const action = data.find(
        (d) => d.host_blue === nodeId || d.host_red === nodeId
      );

      if (action) {
        setDefenderAction(action.blue_action);
        setAttackerAction(action.red_action);
      } else {
        setDefenderAction("No action found");
        setAttackerAction("No action found");
      }
    } catch (error) {
      console.error("Error loading CSV data:", error);
      setDefenderAction("Error loading actions");
      setAttackerAction("Error loading actions");
    }
  };

  return (
    <DrawerContext.Provider
      value={{
        isOpen,
        selectedNode,
        attackerAction,
        defenderAction,
        openDrawer,
        closeDrawer,
      }}
    >
      {children}
    </DrawerContext.Provider>
  );
};

// Custom hook to use the Drawer context
export const useDrawerContext = () => {
  const context = useContext(DrawerContext);
  if (!context) {
    throw new Error("useDrawerContext must be used within a DrawerProvider");
  }
  return context;
};
