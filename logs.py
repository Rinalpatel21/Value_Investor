import json


def log_event(event):

    with open("logs.jsonl", "a") as f:

        f.write(
            json.dumps(
                event,
                default=str      # <- converts unsupported objects to strings
            )
        )

        f.write("\n")