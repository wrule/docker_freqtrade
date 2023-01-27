#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade download-data \
  --exchange binance \
  --days 5000 \
  --timeframes 1m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d \
  --pairs-file user_data/data/binance/pairs.json
