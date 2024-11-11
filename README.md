## Features

<a name="readme-top"></a>
<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]](https://www.linkedin.com/in/chater-marzougui-342125299/)
</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ghassen-fatnassi/CS_TUN56">
    <img src="./images/logo.png" alt="Logo" width="256" height="256">
  </a>
    <h1 width="35px">Soteria</h1>
  <p align="center">
    A Comprehensive Cybersecurity Solution with Multiple Analysis Components
    <br />
    <br />
    <a href="https://github.com/ghassen-fatnassi/CS_TUN56/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/ghassen-fatnassi/CS_TUN56/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#system-architecture">System Architecture</a></li>
    <li><a href="#testing-and-integration">Testing and Integration</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#credits">Credits</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

**Soteria** is an advanced cybersecurity system designed to tackle modern cyber threats using a suite of models and tools. Built with scalability in mind, Soteria is structured as a microservices-based platform that combines reinforcement learning, social media parsing, malware analysis, anomaly detection, traffic logging, and a retrieval-augmented generation (RAG) model. This enables Soteria to address a wide variety of cybersecurity challenges in real time.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Features

Our system, **Soteria**, is an innovative, multi-layered cybersecurity solution designed to address various types of cyber threats. It is structured as a microservices-based platform, allowing for scalability and modularity. Here's a detailed breakdown of each component:

1. **Reinforcement Learning Agent**:
   - **Environment**: Utilizes the CAGE environment to simulate various cybersecurity scenarios.
   - **Graph Neural Network (GNN)**: Integrates a GNN to store and track the system status, enabling communication of critical states.
   - **Message Sending Capabilities**: Implements novel message passing through GNN for system status updates.
   - **Training Flexibility**: Can run in multiple variations without losing accuracy thanks to the GNN architecture.

   <div align="center" width="800">
     <img src="./images/net_architecture.png" alt="Reinforcement Learning Agent" width="800">
   </div>

2. **Twitter Parsing and Threat Detection**:
   - **Threat Analysis**: A logistic regression classifier, combined with a "cyner" instance, assesses threat levels in tweets.
   - **Blacklist Monitoring**: Maintains and monitors a blacklist of user IDs for real-time threat detection.
   - **Real-time Processing**: Processes and analyzes tweets as they are posted for immediate threat assessment.
   - **Comprehensive Monitoring**: Tracks specified users and keywords for potential security threats.

3. **Malware Analysis Tool**:
   - **Static Analysis**: Novel approach of transforming binary data into images for CNN-based analysis.
   - **Dynamic Analysis**: Integration with VirusTotal API for comprehensive malware scanning.
   - **Performance**: Demonstrated exceptional accuracy in malware detection through image-based analysis.
   - **Real-time Detection**: Continuous monitoring and analysis of file system changes.

   <div align="center" width="800">
     <img src="./images/file_analyser.png" alt="Malware Analysis Tool" width="800">
   </div>

4. **HDFS Anomaly Detection**:
   - **Distributed Architecture**: Multiple agents collect logs from HDFS servers.
   - **Centralized Processing**: Centralized manager processes collected data in real-time.
   - **Advanced Model**: LSTM network with deviation layer for accurate anomaly detection.
   - **Real-time Updates**: Continuous frontend updates with detection results.
   - **Scalable Implementation**: Can handle multiple HDFS clusters simultaneously.

5. **Traffic Logging Agent**:
   - **Data Collection**: CICFlowMeter integration for comprehensive traffic data collection.
   - **Endpoint Monitoring**: Collects data from all connected end devices.
   - **Advanced Analytics**: XGBoost/Random Forest voting system for accurate threat prediction.
   - **Centralized Management**: Preprocesses and analyzes data through a central manager.
   - **Real-time Visualization**: Live traffic analysis and threat detection display.

   <div align="center" width="800">
     <img src="./images/dashboard.png" alt="Traffic Logging Agent Dashboard" width="800">
   </div>

6. **Zephyr 7B RAG Model**:
   - **Document Processing**: Parses research papers, logs, and external URL reports.
   - **Contextual Analysis**: Provides intelligent responses to cybersecurity queries.
   - **Integration**: Seamlessly connects with other system components for comprehensive analysis.
   - **Adaptive Learning**: Updates knowledge base with new security information.

   <div align="center" width="800">
     <img src="./images/rag.png" alt="RAG Model" width="800">
   </div>

7. **Comprehensive Frontend**:
   - **Real-time Dashboard**: Displays all system analytics and alerts.
   - **React-based Interface**: Modern, responsive user interface.
   - **Microservices Architecture**: Each component runs in isolated Docker containers.
   - **Orchestration**: Managed through Docker Compose for seamless operation.

   <div align="center" width="800">
     <img src="./images/whole_env.jpg" alt="Frontend Overview" width="800">
   </div>

## System Architecture

- **Microservices Design**: 
  - Each component is containerized independently
  - Individual scaling capabilities
  - Fault isolation and resilience
  - Independent deployment and updates

- **Integration Capabilities**:
  - Compatible with existing cybersecurity tools
  - Seamless integration with Suricata, Wazuh, and Filebeat
  - Extensible plugin architecture
  - Standardized API interfaces

- **Data Flow**:
  - Centralized log collection
  - Real-time data processing
  - Secure communication channels
  - Scalable storage solutions

## Testing and Integration

- **Virtual Environment Testing**:
  - Comprehensive testing with multiple virtual machines
  - Simulated network environments
  - Performance benchmarking
  - Load testing scenarios

- **Security Testing**:
  - Penetration testing conducted
  - Vulnerability assessments
  - Security compliance checking
  - Regular security audits

- **Tool Integration**:
  - Suricata for network monitoring
  - Wazuh for security management
  - Filebeat for log collection
  - Custom integration capabilities

## Installation

### Frontend Installation Guide

The frontend of Soteria is built with **React**, **TypeScript**, and **Vite**. Follow these steps to set it up locally:

#### Prerequisites

1. **Node.js**: Ensure you have Node.js installed (version 16 or higher is recommended).
   - You can download it from [Node.js official website](https://nodejs.org/).

2. **Package Manager**: You can use either **npm** (comes with Node.js) or **yarn**.

#### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ghassen-fatnassi/CS_TUN56
   ```

2. **Navigate to the Frontend Directory**:
   ```bash
   cd CS_TUN56/system/frontend
   ```

3. **Install Dependencies**:
   * If you're using npm:
     ```bash
     npm install
     ```
   * If you're using yarn:
     ```bash
     yarn install
     ```

4. **Configure Environment Variables**:
   * Create a `.env` file in the `frontend` directory
   * Add the following variables, adjusting as needed:
     ```plaintext
     VITE_API_URL=http://localhost:5000 # URL for your backend API
     ```

5. **Start the Development Server**:
   * If you're using npm:
     ```bash
     npm run dev
     ```
   * If you're using yarn:
     ```bash
     yarn dev
     ```

6. **Access the Frontend**:
   * The development server should start on `http://localhost:5173` by default
   * Open this URL in your browser to view the frontend

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

1. Deploy the Soteria system using Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Access the React-based frontend to monitor system status and analytics.

3. For demonstration purposes:
   - Use provided mock data to test system functionality
   - Connect to test virtual machines for live testing
   - Monitor real-time alerts and analytics

4. Integration with existing tools:
   - Configure Suricata for network monitoring
   - Set up Wazuh agents for endpoint security
   - Deploy Filebeat for log collection

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

We welcome contributions to improve Soteria! Please follow these steps:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Credits

Soteria was created by:
- **Mohamed Aziz Badri Khadhraoui**
- **Ghassen Fatnassi**
- **Mohamed Kaouech**
- **Sahar Guebsi**
- **Chater Marzougui**
- **Fatma Ezzahra ben Helal**

And other IEEE SUP'COM Student branch collaborators for the TSYP 2056 CS challenge.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

This project is licensed under the [MIT License](LICENSE).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/ghassen-fatnassi/CS_TUN56.svg?style=for-the-badge
[contributors-url]: https://github.com/ghassen-fatnassi/CS_TUN56/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ghassen-fatnassi/CS_TUN56.svg?style=for-the-badge
[forks-url]: https://github.com/ghassen-fatnassi/CS_TUN56/network/members
[stars-shield]: https://img.shields.io/github/stars/ghassen-fatnassi/CS_TUN56.svg?style=for-the-badge
[stars-url]: https://github.com/ghassen-fatnassi/CS_TUN56/stargazers
[issues-shield]: https://img.shields.io/github/issues/ghassen-fatnassi/CS_TUN56.svg?style=for-the-badge
[issues-url]: https://github.com/ghassen-fatnassi/CS_TUN56/issues
[license-shield]: https://img.shields.io/github/license/ghassen-fatnassi/CS_TUN56.svg?style=for-the-badge
[license-url]: https://github.com/ghassen-fatnassi/CS_TUN56/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/chater-marzougui-342125299
