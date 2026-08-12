#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT}"

if [[ ! -f .env ]]; then
  echo "FATAL: .env missing"
  exit 1
fi
set -a
# shellcheck disable=SC1091
source .env
set +a

if [[ -z "${SITE_DOMAIN:-}" ]]; then
  echo "FATAL: SITE_DOMAIN is required in .env"
  exit 1
fi

COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)

echo "==> Stopping nginx for certbot standalone"
"${COMPOSE[@]}" stop nginx

certbot certonly --standalone \
  -d "${SITE_DOMAIN}" -d "www.${SITE_DOMAIN}" \
  --agree-tos -m "${CERTBOT_EMAIL:?set CERTBOT_EMAIL in .env}" \
  --non-interactive

echo "==> Starting stack with TLS"
export NGINX_CONF="./deploy/nginx/docker.prod.conf"
bash deploy/docker/deploy.sh
