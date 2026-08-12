#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT}"

COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)
SERVICES=(db web nginx)

free_host_ports() {
  echo "==> Freeing host ports 80/443"
  systemctl stop nginx 2>/dev/null || true
  systemctl disable nginx 2>/dev/null || true
  systemctl stop 'gunicorn-*' 2>/dev/null || true
  systemctl disable 'gunicorn-*' 2>/dev/null || true
}

load_env() {
  if [[ ! -f .env ]]; then
    echo "FATAL: .env missing. cp .env.docker.example .env && nano .env"
    exit 1
  fi
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
}

select_nginx_conf() {
  local domain="${SITE_DOMAIN:-}"
  if [[ -n "${domain}" && -f "/etc/letsencrypt/live/${domain}/fullchain.pem" ]]; then
    sed "s/example.com/${domain}/g" deploy/nginx/docker.prod.conf \
      > deploy/nginx/docker.prod.runtime.conf
    export NGINX_CONF="./deploy/nginx/docker.prod.runtime.conf"
    echo "==> TLS cert found for ${domain} → docker.prod.conf"
  else
    export NGINX_CONF="./deploy/nginx/docker.conf"
    echo "==> HTTP-only (no cert yet) → docker.conf"
  fi
}

wait_http_health() {
  local url="${1:-http://127.0.0.1/healthz/}"
  echo "==> Waiting for ${url}"
  local i
  for i in $(seq 1 40); do
    if curl -sf "${url}" >/dev/null 2>&1; then
      echo "==> healthz OK"
      return 0
    fi
    sleep 3
  done
  echo "WARN: healthz not ready yet — check: ${COMPOSE[*]} logs --tail=50 web nginx"
  return 0
}

inventory() {
  echo "==> Service inventory"
  local svc status
  for svc in "${SERVICES[@]}"; do
    status="$("${COMPOSE[@]}" ps --status running -q "${svc}" 2>/dev/null || true)"
    if [[ -n "${status}" ]]; then
      echo "  ${svc}: running"
    else
      echo "  ${svc}: NOT running"
    fi
  done
}

free_host_ports
load_env
select_nginx_conf

echo "==> Build + up"
"${COMPOSE[@]}" build
set +e
"${COMPOSE[@]}" up -d
set -e
"${COMPOSE[@]}" up -d

wait_http_health "http://127.0.0.1/healthz/"
if [[ "${NGINX_CONF}" == *prod* ]]; then
  echo "==> Waiting for https://127.0.0.1/healthz/"
  for i in $(seq 1 20); do
    if curl -skf https://127.0.0.1/healthz/ >/dev/null 2>&1; then
      echo "==> HTTPS healthz OK"
      break
    fi
    sleep 3
  done
fi

inventory
echo "==> Deploy finished"
