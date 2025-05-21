docker compose down
docker volume rm backend_postgres_data
docker compose --env-file .env up -d --build