#!/bin/bash
cd ft_userdata
docker-compose run --rm freqtrade new-strategy \
  --strategy AwesomeStrategy
