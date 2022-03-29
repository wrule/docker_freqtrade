#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade hyperopt \
  --hyperopt-loss OnlyProfitHyperOptLoss \
  --spaces buy roi stoploss trailing \
  --timeframe 15m \
  --pairs BTC/USDT \
  --fee 0.0015 \
  --strategy-path user_data/strategies/jimao \
  --strategy EMACrossed \
  --dry-run-wallet 100 \
  --config user_data/config.json \
  --epochs 400 \
  --job-workers 1
