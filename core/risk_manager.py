def portfolio_stop(
        value,
        initial_capital):

    drawdown = (
        initial_capital -
        value
    ) / initial_capital

    return drawdown >= 0.25