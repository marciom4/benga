#!/usr/bin/env python3
"""Export data from your Garmin Connect account to local JSON files.

Run on your own machine, from the garmin-connect folder:

    python3 export_data.py
    python3 export_data.py --days 30 --activities-limit 100 --download-files

Reuses the session saved by connect.py (~/.garminconnect) — if it's still
valid you won't be asked for a password. Data is written under ./data/,
which is gitignored so it never gets committed.

Garmin rate-limits login and API calls per IP. To stay under that:
- Range endpoints (steps/HR/sleep/etc trends) fetch the whole date range
  in one request instead of one request per day.
- Per-day detail calls and per-activity calls sleep briefly between
  requests and write to disk as they go, so a rate-limit error partway
  through does not lose what was already fetched.
- Defaults are conservative (7 days, 20 activities). Raise them once
  you've confirmed a run completes cleanly.
"""

import argparse
import json
import os
import sys
import time
from datetime import date, timedelta
from getpass import getpass

try:
    from garminconnect import (
        Garmin,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
    )
except ImportError:
    sys.exit("garminconnect is not installed.\nRun: pip install -r requirements.txt")

TOKEN_STORE = os.path.expanduser("~/.garminconnect")
REQUEST_DELAY_SECONDS = 0.4


def prompt_mfa() -> str:
    return input("Garmin sent a code to your email/phone. Enter it here: ").strip()


def get_client() -> Garmin:
    """Resume the cached session; fall back to an interactive login."""
    client = Garmin()
    try:
        client.login(TOKEN_STORE)
        return client
    except Exception:
        pass

    email = os.getenv("GARMIN_EMAIL") or input("Garmin email: ").strip()
    password = os.getenv("GARMIN_PASSWORD") or getpass("Garmin password: ")
    client = Garmin(email, password, prompt_mfa=prompt_mfa)
    client.login(TOKEN_STORE)
    return client


def save_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def call(label: str, fn, *args, **kwargs):
    """Call a Garmin API method, print progress, and never crash the run."""
    try:
        result = fn(*args, **kwargs)
        print(f"  ok  {label}")
        time.sleep(REQUEST_DELAY_SECONDS)
        return result
    except GarminConnectTooManyRequestsError:
        raise
    except Exception as err:
        print(f"  skip {label}: {err}")
        time.sleep(REQUEST_DELAY_SECONDS)
        return None


def export_profile(client: Garmin, out_dir: str) -> None:
    print("Profile & account...")
    profile = {
        "full_name": call("full name", client.get_full_name),
        "user_profile": call("user profile", client.get_user_profile),
        "unit_system": call("unit system", client.get_unit_system),
        "devices": call("devices", client.get_devices),
        "gear": call("gear", client.get_gear),
        "personal_records": call("personal records", client.get_personal_records),
        "active_goals": call("active goals", client.get_active_goals),
        "future_goals": call("future goals", client.get_future_goals),
        "past_goals": call("past goals", client.get_past_goals),
    }
    save_json(os.path.join(out_dir, "profile.json"), profile)


def export_trends(client: Garmin, out_dir: str, start: str, end: str) -> None:
    print(f"Trends {start} to {end} (one request per metric)...")
    trends = {
        "daily_steps": call("daily steps", client.get_daily_steps, start, end),
        "resting_heart_rate": call("resting heart rate", client.get_rhr_daily, start, end),
        "sleep": call("sleep", client.get_sleep_daily, start, end),
        "calories": call("calories", client.get_calories_daily, start, end),
        "body_battery": call("body battery", client.get_body_battery, start, end),
        "hrv": call("HRV", client.get_hrv_data_range, start, end),
        "max_metrics": call("max metrics (VO2 max etc)", client.get_max_metrics_range, start, end),
        "intensity_minutes": call("weekly intensity minutes", client.get_weekly_intensity_minutes, start, end),
    }
    save_json(os.path.join(out_dir, "trends.json"), trends)


def export_daily_details(client: Garmin, out_dir: str, days: int) -> None:
    print(f"Daily details for the last {days} day(s) (one request per metric per day)...")
    for offset in range(days):
        day = (date.today() - timedelta(days=offset)).isoformat()
        print(f" {day}")
        details = {
            "user_summary": call("  user summary", client.get_user_summary, day),
            "stats": call("  stats", client.get_stats, day),
            "steps": call("  steps", client.get_steps_data, day),
            "heart_rates": call("  heart rates", client.get_heart_rates, day),
            "sleep": call("  sleep detail", client.get_sleep_data, day),
            "stress": call("  stress", client.get_all_day_stress, day),
            "respiration": call("  respiration", client.get_respiration_data, day),
            "spo2": call("  SpO2", client.get_spo2_data, day),
            "hydration": call("  hydration", client.get_hydration_data, day),
            "body_composition": call("  body composition", client.get_body_composition, day),
            "training_readiness": call("  training readiness", client.get_training_readiness, day),
            "training_status": call("  training status", client.get_training_status, day),
        }
        save_json(os.path.join(out_dir, "daily", f"{day}.json"), details)


def export_activities(client: Garmin, out_dir: str, limit: int, download_files: bool, activity_format: str) -> None:
    print(f"Activities (up to {limit})...")
    activities = call("activity list", client.get_activities, 0, limit) or []
    save_json(os.path.join(out_dir, "activities.json"), activities)

    for i, activity in enumerate(activities, 1):
        activity_id = activity.get("activityId")
        if activity_id is None:
            continue
        print(f" [{i}/{len(activities)}] activity {activity_id}")
        detail = {
            "summary": activity,
            "detail": call("  detail", client.get_activity, activity_id),
            "splits": call("  splits", client.get_activity_splits, activity_id),
        }
        save_json(os.path.join(out_dir, "activities", f"{activity_id}.json"), detail)

        if download_files:
            try:
                raw = client.download_activity(activity_id, dl_fmt=activity_format)
                ext = {"ORIGINAL": "zip", "TCX": "tcx", "GPX": "gpx", "KML": "kml", "CSV": "csv"}.get(
                    activity_format, "bin"
                )
                files_dir = os.path.join(out_dir, "activities", "files")
                os.makedirs(files_dir, exist_ok=True)
                with open(os.path.join(files_dir, f"{activity_id}.{ext}"), "wb") as f:
                    f.write(raw)
                print(f"  ok  downloaded {activity_format} file")
            except GarminConnectTooManyRequestsError:
                raise
            except Exception as err:
                print(f"  skip download: {err}")
            time.sleep(REQUEST_DELAY_SECONDS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=7, help="How many past days of daily metrics to fetch (default: 7)")
    parser.add_argument("--activities-limit", type=int, default=20, help="Max activities to fetch details for (default: 20)")
    parser.add_argument("--download-files", action="store_true", help="Also download the original activity file for each activity")
    parser.add_argument("--activity-format", default="ORIGINAL", choices=["ORIGINAL", "TCX", "GPX", "KML", "CSV"])
    parser.add_argument("--out", default="data", help="Output directory (default: ./data)")
    args = parser.parse_args()

    if args.days > 90 or args.activities_limit > 100:
        print(
            "Heads up: large ranges make many requests and can trigger Garmin's "
            "rate limit again. If this run gets a 429, wait and re-run with "
            "smaller --days/--activities-limit first.\n"
        )

    print("Connecting to Garmin Connect...")
    try:
        client = get_client()
    except GarminConnectAuthenticationError:
        sys.exit("Login failed: wrong email/password or MFA code.")
    except GarminConnectTooManyRequestsError:
        sys.exit("Too many login attempts. Wait a while and try again.")
    except GarminConnectConnectionError as err:
        sys.exit(f"Could not reach Garmin Connect: {err}")
    print("Connected.\n")

    end = date.today().isoformat()
    start = (date.today() - timedelta(days=args.days)).isoformat()

    try:
        export_profile(client, args.out)
        export_trends(client, args.out, start, end)
        export_daily_details(client, args.out, args.days)
        export_activities(client, args.out, args.activities_limit, args.download_files, args.activity_format)
    except GarminConnectTooManyRequestsError:
        sys.exit(
            "\nGarmin rate-limited this run partway through. Everything fetched "
            "so far is already saved under "
            f"{args.out}/. Wait a while before running again."
        )

    print(f"\nDone. Data saved under {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()
