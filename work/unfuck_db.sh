#/usr/bin/bash

docker stop db
docker system prune -f --all --volumes

docker network create -d bridge backend --label odoo_backend='Yes'

docker run --hostname db --shm-size 8g --restart unless-stopped --network=backend -p 127.0.0.1:5432:5432 -p 127.0.0.1:5433:5433 -e POSTGRES_PASSWORD="admin" -v ./pg-data:/var/lib/postgresql/data --name db -d pgvector/pgvector:pg16-trixie

PGPASSWORD='admin' psql -U postgres -c "CREATE USER admin WITH PASSWORD 'admin';" || true
PGPASSWORD='admin' psql -U postgres -c "ALTER USER admin CREATEDB SUPERUSER"
