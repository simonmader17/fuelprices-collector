# fuelprices-collector

Collects Super 95 (`SUP`) prices for four gas stations around St. Pölten from the official [E-Control fuel price API](https://api.e-control.at/sprit/1.0/doc/) and writes them to the `fuelprices` table in PostgreSQL. In Docker it runs every 30 minutes via cron.

Part of the fuelprices stack, together with [fuelprices-api](https://github.com/simonmader17/fuelprices-api), [fuelprices-svelte](https://github.com/simonmader17/fuelprices-svelte) and [fuelprices-bot](https://github.com/simonmader17/fuelprices-bot).

## Configuration

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `db:5432` | Postgres `host:port` |
| `DATABASE_USERNAME` | `fuelprices` | Postgres user |
| `DATABASE_PASSWORD` | `fuelprices` | Postgres password |

The database name is `fuelprices`. The table is created by fuelprices-api.

## Run locally

```sh
pip install requests psycopg2-binary
DATABASE_URL=localhost:5432 python3 -u fuelprices-collector.py
```

## Docker

```sh
docker build -t simonmader17/fuelprices-collector .
docker compose up -d
```

See [`docker-compose.yml`](docker-compose.yml).
