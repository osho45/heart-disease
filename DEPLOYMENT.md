# Deployment Guide: DigitalOcean

This guide will help you deploy the **Heart Disease Classification** app to a DigitalOcean Droplet.

## Prerequisites
1.  **DigitalOcean Account** (Create one at digitalocean.com).
2.  **SSH Client** (Terminal, PuTTY, or VS Code Remote SSH).
3.  **GitHub Repository**: Ensure you have pushed your code to GitHub as per the README.

---

## Step 1: Create a Droplet (Virtual Machine)

1.  Log in to DigitalOcean Console.
2.  Click **Create** -> **Droplets**.
3.  **Choose Region**: Pick the one closest to you (e.g., New York, San Francisco).
4.  **Choose Image**:
    *   Go to the **Marketplace** tab.
    *   Search for **Docker**.
    *   Select **Docker on Ubuntu**. (This saves you from installing Docker manually).
5.  **Choose Size**:
    *   **Basic** -> **Regular**.
    *   **$6/month (1GB RAM)** is sufficient for this project.
6.  **Authentication**:
    *   **SSH Key** (Recommended): Upload your public key.
    *   **Password**: Create a strong root password.
7.  Click **Create Droplet**.

---

## Step 2: Connect to the Droplet

Wait for the IP address to appear (e.g., `164.x.x.x`).

Open your local terminal:
```bash
ssh root@<YOUR_DROPLET_IP>
```
(Type `yes` if asked to verify authenticity).

---

## Step 3: Deployment

Once inside the server (you'll see a `root@...:` prompt):

1.  **Clone your Repository**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    cd YOUR_REPO_NAME
    ```

2.  **Set Environment Variables (Optional)**:
    If you use DagsHub/MLflow, export your credentials so the app can log remotely:
    ```bash
    export MLFLOW_TRACKING_URI="https://dagshub.com/..."
    export MLFLOW_TRACKING_USERNAME="..."
    export MLFLOW_TRACKING_PASSWORD="..."
    ```

3.  **Start the Application**:
    ```bash
    docker-compose up -d --build
    ```
    *   `-d`: Detached mode (runs in background).
    *   `--build`: Ensures configured images are built.

4.  **Verify Status**:
    ```bash
    docker-compose ps
    ```
    You should see `heart_api` and `heart_ui` with status `Up`.

---

## Step 4: Access Your App

Open your browser:

*   **UI Dashboard**: `http://<YOUR_DROPLET_IP>:8501`
*   **API Documentation**: `http://<YOUR_DROPLET_IP>:8000/docs`

---

## Troubleshooting

*   **"Site can't be reached"**:
    *   Wait 1-2 minutes after starting containers.
    *   Check firewall: `ufw status`. If active, allow ports:
        ```bash
        ufw allow 8000
        ufw allow 8501
        ```
*   **Logs**:
    To see error logs:
    ```bash
    docker-compose logs -f
    ```
