#!/bin/bash
# Newsletter 生成脚本 - 每天早上 9 点跑
DATE=$(date +%Y-%m-%d)
mkdir -p /root/newsletter/output
LOG=/root/newsletter/cron.log

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"; }

log "Fetching GitHub trending..."
cd /root/newsletter
python3 github_trending_real.py "" 15 > trending_${DATE}.json 2>&1

log "Generating newsletter..."
python3 /root/newsletter/newsletter_v3.py

log "Newsletter generated successfully"