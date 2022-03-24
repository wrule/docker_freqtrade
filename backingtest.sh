#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade backtesting \
  --config user_data/config.json \
  --strategy SampleStrategy \
  -i 1m \
  -p BTC/USDT
