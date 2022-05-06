echo "Update"
sudo apt update
echo "Install docker and docker-compose"
sudo apt install -y docker.io docker-compose
echo "Add user to docker group"
sudo usermod -aG docker ${USER}
echo "Install astronomer"
curl -sSL https://install.astronomer.io | sudo bash -s
echo ""
echo "Done! Exit the instance and login again, please!"