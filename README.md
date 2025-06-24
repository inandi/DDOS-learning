# Local DDoS Attack Simulation with Docker

## ⚠️ DISCLAIMER: For Educational Purposes Only ⚠️

**This project is created strictly for learning and educational purposes to understand the principles of Distributed Denial of Service (DDoS) attacks and how systems react under stress. It is designed to be run in a fully isolated, local Docker environment.**

**DO NOT use this project or any of its components to launch attacks against any network, system, or website that you do not own or have explicit, written permission to test. Unauthorized access or attacks are illegal and unethical, and can lead to severe legal consequences.**

**By using this project, you agree to use it responsibly and solely for legitimate, ethical learning within a controlled and isolated environment.**

---

## Table of Contents
1. [About the Project](#about-the-project)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Project Structure](#project-structure)
5. [How to Run](#how-to-run)
6. [Understanding the Attack (Under the Hood)](#understanding-the-attack-under-the-hood)
7. [Observing the Impact](#observing-the-impact)
8. [Example Output & Screenshots](#example-output--screenshots)
9. [Stopping the Attack](#stopping-the-attack)
10. [Further Exploration](#further-exploration)
11. [License](#license)

---

## About the Project

This project provides a simple, self-contained environment to simulate a basic Distributed Denial of Service (DDoS) attack, specifically a SYN flood, against a deliberately vulnerable web server. All components run in Docker containers, ensuring that the simulation is isolated from your host system and external networks. This setup allows you to observe the effects of a DDoS attack on server resources and response times in a safe, controlled learning environment.

---

## Features

- **Victim Server:** Runs a Python Flask web app using Gunicorn with only 1 worker and a very low backlog (2). System-level connection limits are set extremely low, and the container is heavily resource-constrained (CPU and memory). This makes it easy to overwhelm.
- **Attacker Containers:** Use `hping3` to launch a SYN flood attack. You can scale the number of attackers to simulate a distributed attack.
- **Docker Orchestration:** Uses `docker-compose` to easily build, connect, and manage both the victim and attacker containers within a dedicated Docker network.
- **Isolation:** All attack traffic is contained within a private Docker bridge network, preventing any impact on your external network.
- **Observability:** Instructions provided to monitor container logs and resource usage (`docker stats`) to see the attack's impact.

---

## Prerequisites

- **Docker Desktop** (includes Docker Engine and Docker Compose)
    - [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

---

## Project Structure

```
ddos-simulation/
├── docker-compose.yml       # Defines the multi-container application
├── victim/                  # Contains the victim web server application
│   ├── Dockerfile           # Dockerfile for building the victim image
│   └── app.py               # Simple Python Flask web server
└── attacker/                # Contains the DDoS attack tools and script
    ├── Dockerfile           # Dockerfile for building the attacker image (Kali Linux base)
    └── attack.sh            # Script to execute the hping3 SYN flood attack
```

---

## How to Run

1. **Build and start the environment:**
   ```bash
   docker-compose up --build --scale attacker=10 -d
   ```
   - This starts the victim and 10 attacker containers. Increase the number for a stronger attack.

2. **Test the victim site:**
   - Open your browser to `http://localhost/` or use:
     ```bash
     curl -v http://localhost/
     ```
   - Under attack, the site should be very slow or unresponsive.

3. **Monitor logs and stats:**
   - Victim logs:
     ```bash
     docker logs ddos_victim
     ```
   - Resource usage:
     ```bash
     docker stats
     ```

---

## Understanding the Attack (Under the Hood)

This project demonstrates a **SYN Flood** attack:

- **Normal TCP handshake:** Client sends SYN → Server replies SYN-ACK → Client sends ACK.
- **SYN Flood:** Attackers send a huge number of SYN packets but never complete the handshake. The server allocates resources for each half-open connection, quickly exhausting its ability to handle new connections.
- **Victim configuration:**
  - Gunicorn with 1 worker and backlog 2 (very limited concurrent connections)
  - OS-level limits: `net.ipv4.tcp_max_syn_backlog=2`, `net.core.somaxconn=2`
  - Container limits: `cpus: 0.1`, `mem_limit: 64m`
- **Result:** The victim server is easily overwhelmed, leading to timeouts, errors, and worker restarts.

---

## Observing the Impact

- **Victim logs:**
  - Look for lines like:
    ```
    admin@Terminal DDOS-learning % sudo docker logs ddos_victim
    ...
    [CRITICAL] WORKER TIMEOUT (pid:7)
    [ERROR] Error handling request (no URI read)
    [INFO] Worker exiting (pid: 7)
    [INFO] Booting worker with pid: 8
    ```
  - These indicate the server is overwhelmed and unable to process requests.

- **Victim stats:**
  - Use `docker stats` to see high network I/O and memory usage near the limit.
  - Example:
    ```
    admin@Terminal DDOS-learning % sudo docker stats
    CONTAINER ID   NAME                        CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O    PIDS
    f1c125b5cfb0   ddos-learning-attacker-5    104.04%   1.062MiB / 15.61GiB   0.01%     936MB / 1.74GB    0B / 0B      2
    621d0bf4452f   ddos-learning-attacker-8    103.34%   1.055MiB / 15.61GiB   0.01%     940MB / 1.75GB    0B / 0B      2
    3bc9527fcaa7   ddos-learning-attacker-3    103.93%   1.055MiB / 15.61GiB   0.01%     937MB / 1.75GB    0B / 0B      2
    b1ae5a912070   ddos-learning-attacker-6    103.89%   1.055MiB / 15.61GiB   0.01%     939MB / 1.75GB    0B / 0B      2
    52e92b58d627   ddos-learning-attacker-1    102.83%   1.062MiB / 15.61GiB   0.01%     936MB / 1.74GB    0B / 0B      2
    701ee0f500ef   ddos-learning-attacker-2    103.56%   1.059MiB / 15.61GiB   0.01%     938MB / 1.75GB    0B / 0B      2
    01fb4d41361c   ddos-learning-attacker-10   103.88%   1.055MiB / 15.61GiB   0.01%     943MB / 1.76GB    0B / 0B      2
    c2e8585cc493   ddos-learning-attacker-4    103.43%   1.062MiB / 15.61GiB   0.01%     934MB / 1.74GB    0B / 0B      2
    bdc3f8aee841   ddos-learning-attacker-7    103.33%   1.059MiB / 15.61GiB   0.01%     925MB / 1.72GB    0B / 0B      2
    794e61cf5fbd   ddos-learning-attacker-9    103.43%   1.051MiB / 15.61GiB   0.01%     921MB / 1.71GB    0B / 0B      2
    0408da1598f9   ddos_victim                 0.01%     26.11MiB / 64MiB      40.80%    17.4GB / 9.35GB   0B / 131kB   2
    ```

- **Attacker stats:**
  - Each attacker container uses ~100% of a CPU core and sends hundreds of MBs of traffic.

- **Testing responsiveness:**
  - While the attack is running, try:
    ```bash
    curl -v http://localhost/
    ```
  - You should see timeouts, errors, or very slow responses.

- **Network state:**
  - On your host, run:
    ```bash
    sudo netstat -ant | grep :80 | wc -l
    ```
  - This shows how many connections are in progress to port 80.

---

## Example Output & Screenshots

Add your screenshots here to show:
- Victim logs with worker timeouts and errors
- `docker stats` output showing high network I/O and memory usage
- Browser or curl output showing timeouts or errors

---

## Stopping the Attack

To stop all running containers and clean up the Docker network:
```bash
docker-compose down
```

---

## Further Exploration

- **Try different attack types:** Modify `attacker/attack.sh` to use other `hping3` flags for UDP or ICMP floods.
- **Scale attackers:** Increase the number of attacker containers for a stronger effect.
- **Implement defenses:**
  - Add Nginx as a reverse proxy with rate limiting
  - Experiment with firewall rules
  - Add monitoring tools like Prometheus and Grafana
- **Simulate legitimate traffic:** Use tools like `ab`, JMeter, or Locust to generate normal user traffic alongside the attack.