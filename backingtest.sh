#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade backtesting \
  --config user_data/config.json \
  --strategy SampleStrategy \
  --timeframe 5m \
  --pairs BTC/USDT \
  --dry-run-wallet 1000 \
  --breakdown day month \
  > report.txt
