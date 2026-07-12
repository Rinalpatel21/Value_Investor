import numpy as np


def calculate_metrics(
        portfolio_values,
        closed_trades):

    returns = np.diff(
        portfolio_values
    ) / portfolio_values[:-1]

    bars_per_year = 365*48

    annual_factor = np.sqrt(bars_per_year)

    sharpe = (
        np.mean(returns)
        /
        np.std(returns)
    ) * annual_factor
    peak = portfolio_values[0]

    max_drawdown = 0

    for value in portfolio_values:

        peak = max(
            peak,
            value
        )

        drawdown = (
            peak - value
        ) / peak

        max_drawdown = max(
            max_drawdown,
            drawdown
        )

    wins = sum(
        1
        for trade in closed_trades
        if trade["pnl"] > 0
    )

    total = len(closed_trades)

    win_rate = wins / total if total > 0 else 0

    return sharpe, max_drawdown, win_rate