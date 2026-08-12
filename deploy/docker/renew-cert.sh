#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT}"

COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)

echo "==> Stopping nginx for certbot renew"
"${COMPOSE[@]}" stop nginx
certbot renew
"${COMPOSE[@]}" start nginx
"${COMPOSE[@]}" exec nginx nginx -s reload
echo "==> Cert renew done"
