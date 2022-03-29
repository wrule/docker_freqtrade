# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class SRSICrossed(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Optimal timeframe for the strategy.
    timeframe = '2h'

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
      "0": 0.6599999999999999,
      "955": 0.285,
      "2381": 0.107,
      "5081": 0
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.348

    # Trailing stoploss
    trailing_stop = True
    trailing_only_offset_is_reached = True
    trailing_stop_positive = 0.276
    trailing_stop_positive_offset = 0.313  # Disabled / not configured

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }

    @property
    def plot_config(self):
        return {
            # Main plot indicators (Moving averages, ...)
            'main_plot': {
                'tema': {},
                'sar': {'color': 'white'},
            },
            'subplots': {
                # Subplots - each dict defines one additional plot
                "MACD": {
                    'macd': {'color': 'blue'},
                    'macdsignal': {'color': 'orange'},
                },
                "RSI": {
                    'rsi': {'color': 'red'},
                }
            }
        }

    def informative_pairs(self):
      return []

    buy_length = IntParameter(49 - 20, 49 + 20, default = 49)
    buy_rsi_length = IntParameter(2, 30, default = 8)
    buy_k = IntParameter(2, 30, default = 8)
    buy_d = IntParameter(2, 60, default = 27)

    def populate_indicators(
      self,
      dataframe: DataFrame,
      metadata: dict,
    ) -> DataFrame:
      return dataframe

    def populate_buy_trend(
      self,
      dataframe: DataFrame,
      metadata: dict,
    ) -> DataFrame:
      df_kd = pta.stochrsi(
        dataframe['close'],
        length = self.buy_length.value,
        rsi_length = self.buy_rsi_length.value,
        k = self.buy_k.value,
        d = self.buy_d.value,
        append = True,
      )
      k_name = f'STOCHRSIk_{self.buy_length.value}_{self.buy_rsi_length.value}_{self.buy_k.value}_{self.buy_d.value}'
      d_name = f'STOCHRSId_{self.buy_length.value}_{self.buy_rsi_length.value}_{self.buy_k.value}_{self.buy_d.value}'
      dataframe['k'] = df_kd[k_name]
      dataframe['d'] = df_kd[d_name]
      dataframe.loc[
        (
          qtpylib.crossed_above(
            dataframe['k'],
            dataframe['d'],
          ) &
          (dataframe['volume'] > 0)
        ),
        'buy',
      ] = 1
      return dataframe

    def populate_sell_trend(
      self,
      dataframe: DataFrame,
      metadata: dict,
    ) -> DataFrame:
      dataframe.loc[
        (
          qtpylib.crossed_above(
            dataframe['d'],
            dataframe['k'],
          ) &
          (dataframe['volume'] > 0)
        ),
        'sell',
      ] = 1
      return dataframe
