def select_strategy(regime):

    if regime == "TRENDING":

        return "HYBRID"

    elif regime == "RANGING":

        return "DCA_ONLY"

    else:

        return "DCA_ONLY"