#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade hyperopt \
  --hyperopt-loss OnlyProfitHyperOptLoss \
  --spaces buy \
  --timeframe 2h \
  --pairs BTC/USDT \
  --fee 0.0015 \
  --strategy-path user_data/strategies/jimao \
  --strategy SRSICrossed \
  --dry-run-wallet 100 \
  --config user_data/config.json \
  --epochs 4000 \
  --job-workers -2
