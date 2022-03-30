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

class SRSICrossedR(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Optimal timeframe for the strategy.
    timeframe = '2h'

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
      "0": 1e6,
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.99

    # Trailing stoploss
    # trailing_stop = True
    # trailing_only_offset_is_reached = True
    # trailing_stop_positive = 0.276
    # trailing_stop_positive_offset = 0.313  # Disabled / not configured

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

    r_length = 49
    r_rsi_length = 8
    r_k = 8
    r_d = 27
    k_name = f'STOCHRSIk_{r_length}_{r_rsi_length}_{r_k}_{r_d}'
    d_name = f'STOCHRSId_{r_length}_{r_rsi_length}_{r_k}_{r_d}'

    def populate_indicators(
      self,
      dataframe: DataFrame,
      metadata: dict,
    ) -> DataFrame:
      dataframe.ta.stochrsi(
        length = self.r_length,
        rsi_length = self.r_rsi_length,
        k = self.r_k,
        d = self.r_d,
        append = True,
      )
      return dataframe

    def populate_buy_trend(
      self,
      dataframe: DataFrame,
      metadata: dict,
    ) -> DataFrame:
      dataframe.loc[
        (
          qtpylib.crossed_above(
            dataframe[self.k_name],
            dataframe[self.d_name],
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
            dataframe[self.d_name],
            dataframe[self.k_name],
          ) &
          (dataframe['volume'] > 0)
        ),
        'sell',
      ] = 1
      return dataframe
