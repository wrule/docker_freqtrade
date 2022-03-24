#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade backtesting \
  --config user_data/config.json \
  --strategy SampleStrategy \
  --timeframe 1d \
  --pairs BTC/USDT
