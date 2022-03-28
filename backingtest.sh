#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade backtesting \
  --config user_data/config.json \
  --strategy-path user_data/strategies/jimao \
  --strategy SRSICrossed \
  --timeframe 2h \
  --pairs BTC/USDT \
  --dry-run-wallet 100 \
  --fee 0.0015
  # --breakdown month day \
  # --verbose \
  > report.txt
