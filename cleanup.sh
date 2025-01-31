echo "Stopping all running containers..."
docker stop $(docker ps -aq)

echo "Removing all containers..."
docker rm $(docker ps -aq)

echo "Removing all networks..."
docker network prune -f

echo "Removing all volumes..."
docker volume prune -f

echo "Removing all images..."
docker rmi $(docker images -aq) -f

echo "Performing final cleanup..."
docker system prune -af --volumes

echo "Docker cleanup complete!"
