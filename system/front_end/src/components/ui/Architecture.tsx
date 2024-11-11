import { useDrawerContext } from "./DrawerContext";
import * as d3 from "d3";
import React, { useRef, useEffect } from "react";

interface Node extends d3.SimulationNodeDatum {
  id: string;
  name: string;
  type: string;
  status: string;
  rlAgentData: RLAgentData;
}

interface Link extends d3.SimulationLinkDatum<Node> {
  source: string | Node;
  target: string | Node;
  type?: string;
}

interface RLAgentData {
  activityLevel: number;
  lastAction: string;
}

interface NetworkGraph {
  nodes: Node[];
  links: Link[];
}

const data: NetworkGraph = {
  nodes: [
    // Firewalls
    {
      id: "firewall1",
      name: "Firewall Between Subnet 1 and Subnet 2",
      type: "firewall",
      status: "active",
      rlAgentData: { activityLevel: 0.85, lastAction: "Monitoring Traffic" },
    },
    {
      id: "firewall2",
      name: "Firewall Between Subnet 2 and Subnet 3",
      type: "firewall",
      status: "active",
      rlAgentData: { activityLevel: 0.75, lastAction: "Traffic Filtering" },
    },

    // Routers
    {
      id: "router1",
      name: "Router Subnet 1",
      type: "router",
      status: "active",
      rlAgentData: { activityLevel: 0.9, lastAction: "Routing Packets" },
    },
    {
      id: "router2",
      name: "Router Subnet 3",
      type: "router",
      status: "active",
      rlAgentData: { activityLevel: 0.88, lastAction: "Routing Packets" },
    },

    // Switches
    {
      id: "switch1",
      name: "Switch Subnet 1",
      type: "switch",
      status: "active",
      rlAgentData: { activityLevel: 0.7, lastAction: "Distributing Traffic" },
    },
    {
      id: "switch2",
      name: "Switch Subnet 2",
      type: "switch",
      status: "active",
      rlAgentData: { activityLevel: 0.78, lastAction: "Handling Traffic" },
    },
    {
      id: "switch3",
      name: "Switch Subnet 3",
      type: "switch",
      status: "active",
      rlAgentData: { activityLevel: 0.72, lastAction: "Traffic Control" },
    },

    // Servers
    {
      id: "server1",
      name: "Enterprise Server 1",
      type: "server",
      status: "active",
      rlAgentData: { activityLevel: 0.65, lastAction: "Processing Requests" },
    },
    {
      id: "server2",
      name: "Enterprise Server 2",
      type: "server",
      status: "active",
      rlAgentData: { activityLevel: 0.8, lastAction: "Data Analysis" },
    },
    {
      id: "server3",
      name: "Enterprise Server 3",
      type: "server",
      status: "active",
      rlAgentData: { activityLevel: 0.6, lastAction: "Resource Management" },
    },
    {
      id: "operationalServer",
      name: "Operational Server",
      type: "server",
      status: "active",
      rlAgentData: { activityLevel: 0.7, lastAction: "System Coordination" },
    },
    //defender
    {
      id: "defender",
      name: "defender",
      type: "user",
      status: "active",
      rlAgentData: { activityLevel: 0.9, lastAction: "Active Session" },
    },
    // User Hosts
    {
      id: "user1",
      name: "User Host 1",
      type: "user",
      status: "active",
      rlAgentData: { activityLevel: 0.9, lastAction: "Active Session" },
    },
    {
      id: "user2",
      name: "User Host 2",
      type: "user",
      status: "active",
      rlAgentData: { activityLevel: 0.85, lastAction: "Uploading Files" },
    },
    {
      id: "user3",
      name: "User Host 3",
      type: "user",
      status: "active",
      rlAgentData: { activityLevel: 0.88, lastAction: "Downloading Content" },
    },

    // Operational Hosts
    {
      id: "opHost1",
      name: "Operational Host 1",
      type: "user",
      status: "active",
      rlAgentData: { activityLevel: 0.6, lastAction: "Monitoring" },
    },
    {
      id: "opHost2",
      name: "Operational Host 2",
      type: "user",
      status: "active",
      rlAgentData: { activityLevel: 0.7, lastAction: "Data Processing" },
    },
    {
      id: "opHost3",
      name: "Operational Host 3",
      type: "user",
      status: "active",
      rlAgentData: { activityLevel: 0.65, lastAction: "Backup Creation" },
    },
  ],
  links: [
    // Connections in Subnet 1
    { source: "user1", target: "switch1" },
    { source: "user2", target: "switch1" },
    { source: "user3", target: "switch1" },
    { source: "switch1", target: "router1" },

    // Connections from Subnet 1 to Subnet 2
    { source: "router1", target: "firewall1" },
    { source: "firewall1", target: "switch2" },

    // Connections in Subnet 2
    { source: "switch2", target: "server1" },
    { source: "switch2", target: "server2" },
    { source: "switch2", target: "server3" },
    { source: "switch2", target: "defender" },

    // Connections from Subnet 2 to Subnet 3
    { source: "switch2", target: "firewall2" },
    { source: "firewall2", target: "router2" },

    // Connections in Subnet 3
    { source: "router2", target: "switch3" },
    { source: "switch3", target: "operationalServer" },
    { source: "switch3", target: "opHost1" },
    { source: "switch3", target: "opHost2" },
    { source: "switch3", target: "opHost3" },
  ],
};
const App: React.FC = () => {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const { openDrawer } = useDrawerContext();

  useEffect(() => {
    const svgElement = svgRef.current;
    if (!svgElement) return;

    const svg = d3.select(svgElement);
    svg.selectAll("*").remove();

    const width = 1600;
    const height = 1400;

    svg
      .attr("viewBox", `0 0 ${width} ${height}`)
      .style("background-color", "#131a22") // Cyber black background
      .style("border", "1px solid #30c48b"); // Cyber green border

    const simulation = d3
      .forceSimulation<Node>(data.nodes)
      .force(
        "link",
        d3
          .forceLink<Node, Link>(data.links)
          .id((d) => d.id)
          .distance(150)
      )
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg
      .append("g")
      .attr("stroke-opacity", 0.6)
      .selectAll<SVGLineElement, Link>("line")
      .data(data.links)
      .enter()
      .append("line")
      .attr("stroke-width", 2)
      .attr("stroke", "white") // Cyber green for links
      .attr("stroke-dasharray", (d) => (d.type === "dashed" ? "5,5" : ""));

    const node = svg
      .append("g")
      .selectAll<SVGImageElement, Node>("image")
      .data(data.nodes)
      .enter()
      .append("image")
      .attr("xlink:href", (d) => {
        switch (d.type) {
          case "router":
            return "/svgs/router-icon.svg";
          case "switch":
            return "/svgs/switch-icon.svg";
          case "firewall":
            return "/svgs/firewall-icon.svg";
          case "user":
            return "/svgs/user-icon.svg";
          case "server":
            return "/svgs/server-icon.svg";
          default:
            return "/svgs/default-icon.svg";
        }
      })
      .attr("width", 40)
      .attr("height", 40)
      .attr("x", -20)
      .attr("y", -20)
      .call(drag(simulation))
      .on("click", (event, d) => openDrawer(d));

    node.append("title").text((d) => `${d.name} (${d.type})`);

    const tooltip = d3
      .select("body")
      .append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("background", "#222")
      .style("color", "#30c48b")
      .style("padding", "8px")
      .style("border", "1px solid #30c48b")
      .style("border-radius", "4px")
      .style("visibility", "hidden");

    node
      .on("mouseover", (event, d) => {
        tooltip
          .html(
            `<strong>${d.name}</strong><br/>
            Type: ${d.type}<br/>
            Status: ${d.status}<br/>
            Activity Level: ${d.rlAgentData.activityLevel}<br/>
            Last Action: ${d.rlAgentData.lastAction}`
          )
          .style("top", event.pageY - 10 + "px")
          .style("left", event.pageX + 10 + "px")
          .style("visibility", "visible");
      })
      .on("mouseout", () => tooltip.style("visibility", "hidden"));

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => (d.source as Node).x ?? 0)
        .attr("y1", (d) => (d.source as Node).y ?? 0)
        .attr("x2", (d) => (d.target as Node).x ?? 0)
        .attr("y2", (d) => (d.target as Node).y ?? 0);

      node.attr("x", (d) => (d.x ?? 0) - 20).attr("y", (d) => (d.y ?? 0) - 20);
    });

    function drag(
      simulation: d3.Simulation<Node, undefined>
    ): d3.DragBehavior<SVGImageElement, Node, Node> {
      function dragstarted(
        event: d3.D3DragEvent<SVGImageElement, Node, Node>,
        d: Node
      ) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(
        event: d3.D3DragEvent<SVGImageElement, Node, Node>,
        d: Node
      ) {
        d.fx = event.x;
        d.fy = event.y;
      }

      function dragended(
        event: d3.D3DragEvent<SVGImageElement, Node, Node>,
        d: Node
      ) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }

      return d3
        .drag<SVGImageElement, Node, Node>()
        .subject((event, d) => d)
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    }

    return () => {
      simulation.stop();
      tooltip.remove();
    };
  }, []);

  return (
    <div className="centering">
      <h1 style={{ color: "white", marginBottom: "4rem" }}>
        Network Architecture Visualization
      </h1>
      <svg ref={svgRef} width="100%" height="100%"></svg>
    </div>
  );
};

export default App;
