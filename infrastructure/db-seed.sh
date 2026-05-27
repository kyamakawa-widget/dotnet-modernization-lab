#!/usr/bin/env bash
set -euo pipefail
VPS="widget-vps"
echo "==> DB seed data apply"
ssh "$VPS" "PGPASSWORD=demo1234 psql -h 127.0.0.1 -U postgres -d HANBAI" \
  < infrastructure/db/seed/02_seed.sql
echo "==> done"
