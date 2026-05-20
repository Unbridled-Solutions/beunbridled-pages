import json
from datetime import datetime, timedelta, timezone
import sys

def process_airtable_data(airtable_json_str):
    try:
        airtable_data = json.loads(airtable_json_str)
    except json.JSONDecodeError:
        print("[SILENT]")
        return

    new_submissions = []
    now = datetime.now(timezone.utc)
    fifteen_minutes_ago = now - timedelta(minutes=15)

    for record in airtable_data.get("records", []):
        fields = record.get("fields", {})
        status = fields.get("Status")
        submitted_at_str = fields.get("Submitted At")

        if status == "New — Needs Review" and submitted_at_str:
            try:
                submitted_at = datetime.fromisoformat(submitted_at_str.replace("Z", "+00:00"))
                if submitted_at >= fifteen_minutes_ago:
                    new_submissions.append(fields)
            except ValueError:
                continue

    if new_submissions:
        alert_messages = []
        for sub in new_submissions:
            name = sub.get("Name", "N/A")
            business = sub.get("Business Name", "N/A")
            vertical = sub.get("Vertical/Industry", "N/A")
            server_tier = sub.get("Server tier", "N/A")
            telegram_username = sub.get("Telegram Handle", "N/A")

            message = f"Client: {name}\nBusiness: {business}\nVertical: {vertical}\nServer Tier: {server_tier}\nTelegram: {telegram_username}"
            alert_messages.append(message)

        full_alert = "\n\n".join(alert_messages) + "\n\nReady for your review. Reply \'go\' and I\'ll draft their Business DNA."
        print(full_alert)
    else:
        print("[SILENT]")

if __name__ == "__main__":
    process_airtable_data(sys.stdin.read())
