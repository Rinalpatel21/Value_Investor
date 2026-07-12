class Portfolio:

    def __init__(self, initial_cash):

        self.cash = initial_cash

        self.btc_dca = 0

        self.btc_swing = 0

        self.active_trades = []

        self.closed_trades = []

        self.last_dca_buy_price = None

        self.last_dca_buy_time = None

        self.dca_total_cost = 0

        self.dca_avg_cost = 0

        self.dca_protective_sell_active = False

        self.last_trade_time = None

        self.last_atr_buy_time = None

    def total_btc(self):

        return self.btc_dca + self.btc_swing