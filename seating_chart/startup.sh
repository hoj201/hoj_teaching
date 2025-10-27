#!/bin/bash
# startup.sh

# Wait for cloud-init to finish
while [ ! -f /var/lib/cloud/instance/boot-finished ]; do echo 'Waiting for cloud-init...'; sleep 1; done

# --- Install System Dependencies ---
apt-get update
apt-get install -y python3-pip git pipx

# --- Setup App User (Run as 'ubuntu') ---
# We will run the app as the 'ubuntu' user, not as root
export APP_DIR="/home/ubuntu/${app_repo_url}/seating_chart/"
export USER="ubuntu"
export GROUP="ubuntu"

# --- Clone App Repo ---
git clone "${app_repo_url}" "/home/ubuntu/"
chown -R $USER:$GROUP $APP_DIR

# --- Create Virtual Environment & Install Dependencies ---
# We run these commands *as* the 'ubuntu' user
sudo -u $USER bash -c "
pipx ensurepath
pipx install poetry
cd $APP_DIR
poetry install


# --- Create systemd Service File ---
# This file tells the OS how to run and manage our Streamlit app
cat > /etc/systemd/system/streamlit.service << EOF
[Unit]
Description=Streamlit App Service
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=poetry run streamlit run ${app_entrypoint} --server.port 8501 --server.address 0.0.0.0

Restart=always

[Install]
WantedBy=multi-user.target
EOF

# --- Start the Service ---
systemctl daemon-reload
systemctl enable streamlit.service
systemctl start streamlit.service