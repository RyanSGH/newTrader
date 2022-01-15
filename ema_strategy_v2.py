import time
from strategy import Strategy
from basic_data.crypto_trade_get_data.get_position_benifit import get_benifit
from utils.stop_traders import Stop_traders
from basic_data.crypto_trade_get_data.get_position_benifit import get_position
from basic_data.crypto_trade_get_data.get_pending_orderNUM import get_pending_orders
from basic_data.crypto_trade_get_data.get_current_price import fresh_price
from basic_data.crypto_trade_get_data.get_ma import get_ma2
from utils.open_trade import open_trade_thread
from things.position_control.calculate_position import get_balance

class Ema_portfolio_strategy(Strategy.Strategy):
    def __init__(self,Trade_strategy_connection,frequence,trade_num):
        ##frequence 1m 1h
        super().__init__()
        self.Trade_strategy_connection = Trade_strategy_connection
        self.frequence = frequence
        self.trade_num = trade_num

    def _stragegy001a(self):
        Trade_strategy_connection = self.Trade_strategy_connection
        pending_num = self.Trade_strategy_connection.success_pending_order_set
        ma_df = get_ma2(Trade_strategy_connection, self.frequence)
        ma_series = ma_df.iloc[0, [4, 6, 7, 8]]
        self.MA5 = ma_series.MA_5
        self.MA10 = ma_series.MA_10
        self.MA20 = ma_series.MA_20
        self.close = ma_series.close

        print('close')
        print(self.close)
        print('MA10')
        print(self.MA10)

        short_position_num = self.short_position
        long_position_num =
        ###开多
        if (float(self.close) > float(self.MA10)):

            if self.short_position_num == 0:
                bid_price, ask_price = fresh_price(Trade_strategy_connection, "BTC-USD-SWAP")
                Trade_strategy_connection.revoke_order(pending_num)
                #result = open_trade(self.market, ask_price, self.trade_num, 'buy')
                #open_trade_thread(self.Strategy,20,ask_price,self.trade_num,'buy')
                balance, balanceUSD = get_balance(Trade_strategy_connection, 'BTC')
                Trade_strategy_connection.strategy_position = 0.5
                open_trade_thread(Trade_strategy_connection, ask_price, balanceUSD, 'buy',order_type='limit')
        ###开空
        elif float(self.close) < float(self.MA10):

            if self.long_position_num == 0:
                bid_price, ask_price = fresh_price(Strategy, "BTC-USD-SWAP")
                Strategy.revoke_order(pending_num)
                balance, balanceUSD = get_balance(Trade_strategy_connection, 'BTC')
                Trade_strategy_connection.strategy_position = 0.5
                open_trade_thread(Trade_strategy_connection, bid_price, balanceUSD, 'sell', order_type='limit')

        else:
            pass


    def _stragegy001b(self):
        #total_short_benifit = get_benifit(self.Strategy, "short")
        #total_long_benifit = get_benifit(self.Strategy, "long")
        ##平多
        if int(self.long_position_num) != 0:
            if float(self.close) < float(self.MA10)*0.996:
                Stop_traders(self.Trade_strategy_connection, self.trade_num)._stop_long_trade(4)

        ##平空
        if int(self.short_position_num) != 0:
            if float(self.close) > float(self.MA10)*1.004:
                Stop_traders(self.Trade_strategy_connection, self.trade_num)._stop_short_trade(4)

    def strategy_run(self,n):
        '''''
        每n秒执行一次
        '''
        #gdt = get_data_from_sina()
        while True:
            print(time.strftime('%Y-%m-%d %X',time.localtime()))
            try:
                self._stragegy001a()
                self._stragegy001b()
            except Exception as e:
                print(e)
            time.sleep(n)



