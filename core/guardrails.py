def validate_trade(decision, market_context):
    """
    Validate AI decisions before execution.
    Returns:
        (approved, reason)
    """

    tool = decision["decision"]["tool"]

    if tool == "hold":
        return True, "Hold approved."

    if tool == "market_buy":

        amount = decision["decision"].get("amount", 0)

        if amount <= 0:
            return False, "Buy amount must be positive."

        if amount > market_context["cash"]:
            return False, "Not enough cash."

        if amount > market_context["max_buy_amount"]:
            return False, "Buy exceeds risk limit."

        return True, "Buy approved."

    if tool == "market_sell":

        quantity = decision["decision"].get("quantity", 0)

        if quantity <= 0:
            return False, "Quantity must be positive."

        if quantity > market_context["btc"]:
            return False, "Trying to sell more BTC than owned."

        if quantity > market_context["max_sell_quantity"]:
            return False, "Sell exceeds risk limit."

        return True, "Sell approved."

    return False, f"Unknown tool: {tool}"


OFF_TOPIC = [
    "weather",
    "movie",
    "football",
    "basketball",
    "soccer",
    "recipe",
    "cooking",
    "girlfriend",
    "boyfriend",
    "politics",
    "president",
    "religion",
    "doctor",
    "medical",
    "health",
    "homework",
    "math",
    "history",
    "essay",
    "vacation",
    "travel",
    "hotel",
    "restaurant",
    "joke",
    "story",
    "poem",
    "translate",
    "code in java",
    "python tutorial"
]

def is_off_topic(prompt):

    prompt = prompt.lower()

    return any(word in prompt for word in OFF_TOPIC)