from datetime import datetime, timezone

from dotenv import load_dotenv
import os

from luma_sdk.luma_client import LumaClient

load_dotenv()

client = LumaClient(os.getenv("LUMA_API_KEY"))

now = datetime.now(timezone.utc)
upcoming = list(client.list_events(after=now.isoformat(timespec="milliseconds").replace("+00:00", "Z"), sort_column="start_at", sort_direction="asc"))

print(f"Fetch.ai upcoming events ({len(upcoming)} total):\n")
for event in upcoming:
    print(f"  {event.start_at.strftime('%Y-%m-%d')}  {event.name}")
    print(f"           {event.url}")
    print()