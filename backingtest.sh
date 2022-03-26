#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade backtesting \
  --config user_data/config.json \
  --strategy AwesomeStrategy \
  --timeframe 15m \
  --pairs BTC/USDT \
  --dry-run-wallet 1000 \
  # --breakdown day month \
  # --verbose \
  > report.txt
