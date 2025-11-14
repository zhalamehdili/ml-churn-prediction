# Docker Guide

This project uses Docker and Docker Compose to run the FastAPI service and PostgreSQL database in isolated containers. The API, database, model files and logs are fully containerized.

## Quick Start

To start all services:
`docker-compose up -d`

Check API health:
`curl http://localhost:8000/health`

Open API docs:
`open http://localhost:8000/docs`

## Common Commands

### Starting and Stopping

Start in foreground:
`docker-compose up`

Start in background:
`docker-compose up -d`

Stop containers:
`docker-compose down`

Stop and delete all volumes (removes database):
`docker-compose down -v`

### Viewing Logs

All services:
`docker-compose logs`

Follow logs live:
`docker-compose logs -f`

API only:
`docker-compose logs -f api`

Database only:
`docker-compose logs -f db`

Last 50 lines:
`docker-compose logs --tail=50`

### Rebuilding

Rebuild after code changes:
`docker-compose up -d --build`

Force rebuild without cache:
`docker-compose build --no-cache`
`docker-compose up -d`

## Database Access

Open PostgreSQL shell:
`docker exec -it churn-postgres psql -U churnuser -d churn_db`

Run SQL query:
`docker exec -it churn-postgres psql -U churnuser -d churn_db -c "SELECT COUNT(*) FROM prediction_logs;"`

Backup database:
`docker exec churn-postgres pg_dump -U churnuser churn_db > backup.sql`

Restore database:
`docker exec -i churn-postgres psql -U churnuser -d churn_db < backup.sql`

## Troubleshooting

Check running containers:
`docker-compose ps`

Inspect container:
`docker inspect churn-api`

Live resource usage:
`docker stats`

Remove stopped containers:
`docker-compose rm`

Remove all unused Docker resources:
`docker system prune -a`

## Development Workflow

### Code Changes

1. Edit code in the src/ directory
2. Rebuild containers using `docker-compose up -d --build`
3. Test the API at http://localhost:8000/docs
4. Check logs with `docker-compose logs -f api`

### Running Tests

Run tests inside Docker:
`docker-compose exec api pytest tests/ -v`

With coverage:
`docker-compose exec api pytest tests/ --cov=src`

## Production Tips

### Environment Variables

Use a .env file or define variables in docker-compose:
`DATABASE_URL`
`SECRET_KEY`

### Resource Limits Example

Set resource limits in docker-compose:
`cpus: "0.5"`
`memory: 512M`

### Health Checks

Check health status:
`docker inspect churn-api | grep Health -A 10`

## Volumes

- postgres_data: persistent DB storage
- ./models: model artifacts
- ./logs: API logs

## Network

Containers run on the churn-network bridge network.
API reaches PostgreSQL at `db:5432`.