import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


def load_sheet_config():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "service_account.json",
        scope
    )

    client = gspread.authorize(creds)

    sheet = client.open(
        "BTC_AGENT_CONFIG"
    ).sheet1

    data = sheet.get_all_records()

    config = {}

    for row in data:

        config[row["Parameter"]] = float(row["Value"])

    return config