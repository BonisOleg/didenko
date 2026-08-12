#!/usr/bin/env bash
set -euo pipefail

if command -v docker >/dev/null 2>&1; then
  echo "==> Docker already installed"
  docker --version
  docker compose version
  exit 0
fi

echo "==> Installing Docker Engine"
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker

if [[ -n "${SUDO_USER:-}" ]]; then
  usermod -aG docker "${SUDO_USER}"
elif [[ -n "${USER:-}" && "${USER}" != "root" ]]; then
  usermod -aG docker "${USER}"
fi

docker --version
docker compose version
echo "==> Log out/in if docker group was just added"
