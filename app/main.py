from luma_sdk.luma_client import LumaClient
from dotenv import load_dotenv
import os

load_dotenv()

LUMA_API_KEY = os.getenv("LUMA_API_KEY")

client = LumaClient(LUMA_API_KEY)
event = client.get_event("evt-eJuh3dgMEiJ2MUj")
print(event)