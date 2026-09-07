#!/usr/bin/env python3
"""Non-interactive Garmin Connect snapshot for scheduled routines.

Unlike connect.py / export_data.py (built for a human typing a password in
their own terminal), this script is meant to run unattended inside a
scheduled routine. It reads credentials from the GARMIN_EMAIL and
GARMIN_PASSWORD environment variables — set those in your Claude Code
environment settings, never pass them in chat or hardcode them here.

If login fails for any reason (missing env vars, Garmin asking for an MFA
code with no one to answer it, a rate limit, a network error), this prints
a one-line reason to stderr and exits non-zero instead of hanging or
crashing with a traceback. The calling routine should treat that as "no
Garmin data today" and continue rather than stop the whole briefing.

On success, prints a single JSON object to stdout with recent recovery/
training metrics (sleep, stress, body battery, training readiness/status,
HRV, VO2max trend, resting heart rate).
"""

import json
import os
import sys
from datetime import date, timedelta

try:
    from garminconnect import (
        Garmin,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
    )
except ImportError:
    sys.exit("garminconnect is not installed. Run: pip install garminconnect curl_cffi")


def _mfa_unavailable() -> str:
    raise RuntimeError("Garmin asked for an MFA code, but this is an unattended run")


def safe(fn, *args):
    try:
        return fn(*args)
    except Exception:
        return None


def main() -> None:
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    if not email or not password:
        sys.exit("GARMIN_EMAIL/GARMIN_PASSWORD not set, skipping Garmin data")

    client = Garmin(email, password, prompt_mfa=_mfa_unavailable)
    try:
        client.login()
    except (
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
        RuntimeError,
    ) as err:
        sys.exit(f"Garmin login failed, skipping Garmin data: {err}")

    today = date.today().isoformat()
    week_ago = (date.today() - timedelta(days=7)).isoformat()

    heart_rates = safe(client.get_heart_rates, today) or {}
    snapshot = {
        "date": today,
        "resting_heart_rate": heart_rates.get("restingHeartRate"),
        "sleep": safe(client.get_sleep_data, today),
        "stress": safe(client.get_all_day_stress, today),
        "body_battery": safe(client.get_body_battery, week_ago, today),
        "training_readiness": safe(client.get_training_readiness, today),
        "training_status": safe(client.get_training_status, today),
        "hrv": safe(client.get_hrv_data_range, week_ago, today),
        "vo2max_trend": safe(client.get_max_metrics_range, week_ago, today),
    }
    print(json.dumps(snapshot, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
