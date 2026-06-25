from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("EMAIL_ADDRESS"))
print(os.getenv("EMAIL_PASSWORD"))