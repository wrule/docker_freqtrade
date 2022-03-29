from pandas import DataFrame
from functools import reduce
import talib.abstract as ta
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, IStrategy, IntParameter)
import freqtrade.vendor.qtpylib.indicators as qtpylib

class EMACrossed(IStrategy):
  stoploss = -0.05
  timeframe = '2h'
  buy_ema_short = IntParameter(2, 80, default = 5)
  buy_ema_long = IntParameter(2, 200, default = 50)

  def populate_indicators(
    self,
    dataframe: DataFrame,
    metadata: dict,
  ) -> DataFrame:
    for val in self.buy_ema_short.range:
      dataframe[f'ema_short_{val}'] = ta.EMA(dataframe, timeperiod = val)
    for val in self.buy_ema_long.range:
      dataframe[f'ema_long_{val}'] = ta.EMA(dataframe, timeperiod = val)
    return dataframe

  def populate_buy_trend(
    self,
    dataframe: DataFrame,
    metadata: dict,
  ) -> DataFrame:
    conditions = []
    conditions.append(
      qtpylib.crossed_above(
        dataframe[f'ema_short_{self.buy_ema_short.value}'], dataframe[f'ema_long_{self.buy_ema_long.value}']
      )
    )
    conditions.append(dataframe['volume'] > 0)
    if conditions:
      dataframe.loc[
        reduce(lambda x, y: x & y, conditions),
        'buy'
      ] = 1
    return dataframe

  def populate_sell_trend(
    self,
    dataframe: DataFrame,
    metadata: dict,
  ) -> DataFrame:
    conditions = []
    conditions.append(
      qtpylib.crossed_above(
        dataframe[f'ema_long_{self.buy_ema_long.value}'], dataframe[f'ema_short_{self.buy_ema_short.value}']
      )
    )
    conditions.append(dataframe['volume'] > 0)
    if conditions:
      dataframe.loc[
        reduce(lambda x, y: x & y, conditions),
        'sell'
      ] = 1
    return dataframe
