#!/bin/bash
export PATH="/root/.nvm/versions/node/v22.22.1/bin:$PATH"
cd /root/newsletter
DATE=$(date +%Y-%m-%d)
LOG=/root/newsletter/cron.log

echo "[$(date)] Generating newsletter..." >> $LOG
bash /root/newsletter/generate_newsletter.sh >> $LOG 2>&1

echo "[$(date)] Generating social content..." >> $LOG
python3 /root/newsletter/social/gen_social.py $DATE >> $LOG 2>&1

echo "[$(date)] Generating cover image..." >> $LOG
python3 /root/newsletter/social/gen_cover.py $DATE >> $LOG 2>&1
cp /root/newsletter/social/wechat_headline_${DATE}.png /root/newsletter/social/wechat_headline_final.png

echo "[$(date)] Pushing to Feishu..." >> $LOG
python3 /root/newsletter/feishu_push.py $DATE >> $LOG 2>&1

echo "[$(date)] Sending image to Feishu..." >> $LOG
node /root/newsletter/feishu_send_image.js $DATE >> $LOG 2>&1

echo "[$(date)] Publishing to WeChat draft..." >> $LOG
python3 /root/newsletter/wechat_draft.py $DATE >> $LOG 2>&1

echo "[$(date)] Done" >> $LOG
