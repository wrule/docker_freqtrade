#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade backtesting \
  --config user_data/config.json \
  --strategy AwesomeStrategy \
  --timeframe 2h \
  --pairs BTC/USDT \
  --dry-run-wallet 1000 \
  # --breakdown day month \
  --breakdown month \
  # --verbose \
  > report.txt
