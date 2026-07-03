import json
from datetime import datetime


def log_event(event):

    event["timestamp"] = str(datetime.now())

    with open(
        "agent_log.jsonl",
        "a"
    ) as f:

        f.write(json.dumps(event))

        f.write("\n")