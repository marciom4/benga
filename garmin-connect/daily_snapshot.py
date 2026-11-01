#!/usr/bin/env python3
"""Non-interactive Garmin snapshot for scheduled routines.

Uses Garmin's official Personal API client (not a reverse-engineered login),
so there's no password, no MFA prompt, and no bot-detection cat-and-mouse —
just a single API key. Reads it from the GARMIN_PERSONAL_API_KEY environment
variable, which you set in your Claude Code environment settings. Never pass
it in chat or hardcode it here.

Create the key at Garmin Connect -> Settings -> "Chave de API pessoal"
(https://connect.garmin.com/app/settings/personalApiToken). Keys expire
(30-365 days, your choice); Garmin emails a reminder about a week before.

If the key is missing, expired, or revoked, this prints a one-line reason to
stderr and exits non-zero instead of crashing — the calling routine should
treat that as "no Garmin data today" and continue.

On success, prints a single JSON object to stdout with recent recovery/
training metrics (sleep, stress, body battery, HRV, resting heart rate,
fitness age).
"""

import json
import os
import sys
from datetime import date, timedelta

try:
    from garmin_personal_api import GarminPersonalApiClient, PersonalApiAuthenticator
except ImportError:
    sys.exit("garmin-connect-personal-api-python is not installed. Run: pip install -r requirements.txt")


def safe(fn, *args):
    try:
        return fn(*args)
    except Exception:
        return None


def main() -> None:
    api_key = os.getenv("GARMIN_PERSONAL_API_KEY")
    if not api_key:
        sys.exit("GARMIN_PERSONAL_API_KEY not set, skipping Garmin data")

    try:
        with PersonalApiAuthenticator() as authenticator:
            token = authenticator.obtain_token(api_key)
    except Exception as err:
        sys.exit(f"Garmin login failed, skipping Garmin data: {err}")

    today = date.today().isoformat()
    week_ago = (date.today() - timedelta(days=7)).isoformat()

    with GarminPersonalApiClient(token.access_token) as client:
        snapshot = {
            "date": today,
            "heart_rate": safe(client.get_daily_heart_rate, today),
            "sleep": safe(client.get_daily_sleep, today),
            "stress": safe(client.get_daily_stress, today, today),
            "body_battery": safe(client.get_daily_body_battery, week_ago, today),
            "hrv": safe(client.get_daily_hrv, today),
            "fitness_age": safe(client.get_fitness_age, today),
        }

    print(json.dumps(snapshot, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
