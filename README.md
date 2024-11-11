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

1. **Reinforcement Learning Agent**:
   - Utilizes the CAGE environment with a Graph Neural Network (GNN) for system status tracking.
   - Trains agents across multiple scenarios without accuracy loss.

<div align="center" width="800">
  <img src="./images/net_architecture.png" alt="Malware Analysis Tool" width="800">
</div>

2. **Twitter Parsing and Threat Detection**:
   - Extracts tweets and analyzes threat levels with a logistic regression classifier.
   - Monitors blacklisted user accounts for real-time threat detection.

3. **Malware Analysis Tool**:
   - Static analysis using a CNN that processes binary data as images.
   - Dynamic analysis supported by VirusTotal integration.

<div align="center" width="800">
  <img src="./images/file_analyser.png" alt="Malware Analysis Tool" width="800">
</div>

4. **HDFS Anomaly Detection**:
   - Collects logs from HDFS servers via multiple agents.
   - LSTM-based model with deviation layer for real-time anomaly detection.

5. **Traffic Logging Agent**:
   - Uses CICFlowMeter for traffic data collection from endpoints.
   - Centralized XGBoost/Random Forest voting system for predictions.

<div align="center" width="800">
  <img src="./images/dashboard.png" alt="Malware Analysis Tool" width="800">
</div>

6. **Zephyr 7B RAG Model**:
   - Capable of parsing research papers, logs, and external reports.
   - Answers questions using contextual understanding.
   
<div align="center" width="800">
  <img src="./images/rag.png" alt="Malware Analysis Tool" width="800">
</div>


7. **Comprehensive Frontend**:
   - Built with React, displaying all relevant data and analytics.
   - Microservices architecture with Docker for scalability and orchestration.

<div align="center" width="800">
  <img src="./images/whole_env.jpg" alt="Malware Analysis Tool" width="800">
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation

To set up Soteria locally, follow these steps:

1. Clone the repository: `git clone https://github.com/ghassen-fatnassi/CS_TUN56`
2. Navigate to the project directory: `cd CS_TUN56`
3. Ensure Docker and Docker Compose are installed.
4. Run the services: `docker-compose up --build`

For each module, additional dependencies and configurations are specified in the respective README sections or Dockerfiles.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

1. Deploy the Soteria system using Docker Compose.
2. Access the React-based frontend to monitor system status and analytics.
3. For demonstration, preloaded mock data can be fed into the models to observe functionality.
4. Logs and alerts will display in real time, with threat levels, anomalies, and other cybersecurity events highlighted.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

We welcome contributions to improve Soteria! Please fork the repository and create a pull request for any new features or fixes. Contributions can also be submitted as issues.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Credits

Soteria was created by **Mohamed Aziz Badri Khadhraoui, Ghassen Fatnassi, Mohamed Kaouech, Sahar Guebsi, Chater Marzougui, Fatma Ezzahra ben Helal** and collaborators for the TSYP 2056 CS challenge.

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
