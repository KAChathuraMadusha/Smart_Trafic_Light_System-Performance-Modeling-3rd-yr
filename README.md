# Smart Traffic Light Simulation

## Overview
This project simulates traffic flow at a single intersection using **SimPy**, a Python-based discrete-event simulation framework.  
The simulation measures performance metrics such as **average wait time**, **throughput**, and **vehicles served** for different traffic configurations and control strategies.

---

## Features
- Simulates vehicle arrivals using a **Poisson process**.
- Models multiple lanes as **resources**; vehicles wait if lanes are occupied.
- Supports **Fixed** and **Adaptive** traffic control strategies:
  - **Fixed:** Normal service time
  - **Adaptive:** Reduces service time by 20% to optimize traffic flow
- Collects performance metrics:
  - Average wait time per vehicle
  - Throughput (vehicles/sec)
  - Vehicles served per hour
- Generates **visualizations** for experiments:
  - Average wait time
  - Throughput
  - Vehicles served
- Fully **interactive**: Users can define traffic levels (Light, Medium, Heavy) and experiment parameters.

---

## Installation
1. Clone the repository:
```bash
git clone <your-repo-url>
