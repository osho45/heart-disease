# Deployment Guide: Google Cloud Platform (GCP)

Follow these specific steps to deploy the application on a GCP VM (Debian).

## 1. Create a GCP VM
1.  Go to **GCP Console** → **Compute Engine** → **VM instances**.
2.  Click **Create instance**.
3.  **OS**: Choose **Debian** (default).
4.  **Machine Type**: Keep default or choose `e2-small`/`e2-medium`.
5.  Click **Create**.

## 2. Add Network Tag to the VM
1.  In **VM instances**, click on your new VM's name.
2.  Click **Edit**.
3.  Scroll down to **Network tags**.
4.  Add the tag: `ml-demo`
5.  Click **Save**.

## 3. Create Firewall Rule
1.  Go to **VPC network** → **Firewall**.
2.  Click **Create firewall rule**.
3.  **Name**: `allow-ml-demo-ports`
4.  **Direction**: Ingress
5.  **Targets**: Specified target tags
6.  **Target tag**: `ml-demo`
7.  **Source IPv4 ranges**: `0.0.0.0/0` (allows access from anywhere)
8.  **Protocols and ports**:
    *   Check **TCP** and enter: `8000, 8501`
9.  Click **Create**.

## 4. SSH into the VM
1.  Go back to **VM instances**.
2.  Click the **SSH** button next to your VM instance (opens browser terminal).

## 5. Install Docker + Docker Compose v2 (Debian)
Run the following commands in the VM terminal to set up Docker:

```bash
# Update repositories and install basics
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg git

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up the Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and Compose
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Run Docker without sudo (optional, but convenient)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

## 6. Clone Application Code
```bash
cd ~
# Replace with YOUR repository URL if different
git clone https://github.com/osho45/heart-disease.git
cd heart-disease
```

## 7. Configuration (.env)
Create an environment file (optional if not using DagsHub, but good practice):

```bash
cat > .env << 'EOF'
MLFLOW_TRACKING_URI=
MLFLOW_TRACKING_USERNAME=
MLFLOW_TRACKING_PASSWORD=
EOF
```
*(Fill in the values if you have them, otherwise leave blank)*.

## 8. Check Models
Confirm the model file exists (it should have been cloned if you added it to git):
```bash
ls -la models
```

## 9. Build and Run
Start the application containers:
```bash
docker compose up -d --build
```
Check status:
```bash
docker ps
```

## 10. Verify Locally (on VM)
```bash
curl -I http://localhost:8000/docs
curl -I http://localhost:8501
```
*(Should return HTTP 200 OK)*

## 11. Access from Your Laptop
Use the **External IP** of your VM (found in the GCP Console VM list):

*   **Streamlit UI**: `http://<VM_EXTERNAL_IP>:8501`
*   **FastAPI Docs**: `http://<VM_EXTERNAL_IP>:8000/docs`
