# ETL Pipeline with Docker Swarm & Multipass

This project implements a simple **ETL pipeline** using **Docker Swarm**, deployed on **three virtual machines (1 manager, 2 workers)** created with **Multipass**.

It demonstrates containerized data processing, service orchestration, shared volumes, and PostgreSQL persistence in a multi-node environment.

---

## Architecture Overview

### Services

| Service | Role | Description |
|------|------|------------|
| **backend** | Extract | Generates CSV data files |
| **ingester** | Load | Reads CSV files and loads them into PostgreSQL |
| **db** | Storage | PostgreSQL database |

### Infrastructure

- **Multipass VMs**
  - `manager`
  - `worker1`
  - `worker2`
- **Docker Swarm** for orchestration
- **Named volumes** for persistence and data sharing

---

## 📂 Project Structure

etl-swarm/

├── backend/ # Extract service: CSV generation

├── ingester/ # Load service: PostgreSQL ingestion

├── data/ # Shared data between services

│ └── init.sql # PostgreSQL initialization script

├── .env # Environment variables

└── stack-etl.yml # Docker Swarm stack definition

---

## ETL Flow

backend ──► shared-data volume ──► ingester ──► PostgreSQL

- The **backend** service generates CSV files into a shared volume
- The **ingester** service reads these files and inserts the data into PostgreSQL
- PostgreSQL data is persisted using a dedicated volume

---

## Volumes

| Volume | Purpose |
|------|--------|
| `shared-data` | Shared CSV files between backend and ingester |
| `pgdata` | PostgreSQL persistent data |

Volumes are **Docker-managed** and stored on the Swarm nodes.

## Deployment Guide

### 1-Create Multipass VMs

```bash
multipass launch --name manager
multipass launch --name worker1
multipass launch --name worker2
```

### 2-Install Docker on each VM
Run on each VM:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ubuntu
```


### 3-Initialize Docker Swarm (manager node)

```bash
docker swarm init
```

```bash
docker swarm join --token <token> <manager-ip>:2377
```


### 4-Mount the project into the manager VM

```bash
multipass mount ~/projects/etl-swarm manager:/home/ubuntu/etl-swarm
Docker bind mounts must reference paths inside the VM, not the host OS.
```

### 5-Deploy the stack

```bash
cd /home/ubuntu/etl-swarm
docker stack deploy -c stack-etl.yml etl
```

Useful Commands
```bash
docker stack services etl
docker service ps etl_backend
docker service logs etl_ingester
docker volume ls
```


Environment Variables
Environment variables are defined in the .env file:

POSTGRES_USER

POSTGRES_PASSWORD

POSTGRES_DB


### Key Concepts Demonstrated

-Docker Swarm orchestration

-Multi-node deployment with Multipass

-Named volumes for persistence

-Shared volumes for ETL pipelines

-Separation of extract and load responsibilities



Notes

The deploy section in stack-etl.yml is only effective in Docker Swarm

PostgreSQL initialization scripts run only on first startup

Removing volumes will delete all persisted data


License

This project is provided for learning and demonstration purposes.