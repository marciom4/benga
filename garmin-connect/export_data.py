#!/usr/bin/env python3
"""Export data from your Garmin account to local JSON files.

Uses Garmin's official Personal API client. Run on your own machine, from
the garmin-connect folder:

    python3 export_data.py
    python3 export_data.py --days 30 --activities-limit 100 --download-files

Reads the API key from GARMIN_PERSONAL_API_KEY (or prompts via getpass if
unset). Data is written under ./data/, which is gitignored so it never gets
committed.

Garmin documents no rate limit for the Personal API, but some endpoints cap
how far back a single range request can go (e.g. ~28 days for steps, ~31 for
sleep). Defaults here (7 days / 20 activities) stay well under that; raise
them once a run completes cleanly.
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta
from getpass import getpass

try:
    from garmin_personal_api import GarminPersonalApiClient, PersonalApiAuthenticator
except ImportError:
    sys.exit("garmin-connect-personal-api-python is not installed.\nRun: pip install -r requirements.txt")


def get_client() -> GarminPersonalApiClient:
    api_key = os.getenv("GARMIN_PERSONAL_API_KEY") or getpass("Garmin personal API key: ")
    with PersonalApiAuthenticator() as authenticator:
        token = authenticator.obtain_token(api_key)
    return GarminPersonalApiClient(token.access_token)


def save_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def call(label: str, fn, *args, **kwargs):
    """Call a Garmin API method, print progress, and never crash the run."""
    try:
        result = fn(*args, **kwargs)
        print(f"  ok  {label}")
        return result
    except Exception as err:
        print(f"  skip {label}: {err}")
        return None


def export_profile(client: GarminPersonalApiClient, out_dir: str) -> None:
    print("Profile...")
    profile = {
        "profile_settings": call("profile settings", client.get_user_profile_settings),
        "heart_rate_zones": call("heart rate zones", client.get_heart_rate_zones),
    }
    save_json(os.path.join(out_dir, "profile.json"), profile)


def export_trends(client: GarminPersonalApiClient, out_dir: str, start: str, end: str) -> None:
    print(f"Trends {start} to {end} (one request per metric)...")
    trends = {
        "daily_summaries": call("daily summaries", client.get_daily_summaries, start, end),
        "steps": call("steps", client.get_daily_steps, start, end),
        "sleep_summaries": call("sleep summaries", client.get_daily_sleep_summaries, start, end),
        "hrv_summaries": call("HRV summaries", client.get_daily_hrv_summaries, start, end),
        "body_battery": call("body battery", client.get_daily_body_battery, start, end),
        "stress": call("stress", client.get_daily_stress, start, end),
        "hydration": call("hydration", client.get_daily_hydration, start, end),
        "weight_measurements": call("weight measurements", client.get_weight_measurements, start, end),
        "weight_goals": call("effective weight goals", client.get_effective_weight_goals, start, end),
        "wellness_activities": call("wellness activity summaries", client.get_wellness_activity_summaries, start, end),
    }
    save_json(os.path.join(out_dir, "trends.json"), trends)


def export_daily_details(client: GarminPersonalApiClient, out_dir: str, days: int) -> None:
    print(f"Daily details for the last {days} day(s) (single-day-only metrics)...")
    for offset in range(days):
        day = (date.today() - timedelta(days=offset)).isoformat()
        print(f" {day}")
        details = {
            "heart_rate": call("  heart rate", client.get_daily_heart_rate, day),
            "sleep": call("  sleep detail", client.get_daily_sleep, day),
            "hrv": call("  HRV", client.get_daily_hrv, day),
            "spo2": call("  SpO2", client.get_daily_spo2, day),
            "fitness_age": call("  fitness age", client.get_fitness_age, day),
        }
        save_json(os.path.join(out_dir, "daily", f"{day}.json"), details)


def export_activities(client: GarminPersonalApiClient, out_dir: str, limit: int, download_files: bool) -> None:
    print(f"Activities (up to {limit})...")
    result = call("activity list", client.search_activities, limit=limit) or {}
    activities = result.get("results", result) if isinstance(result, dict) else result
    save_json(os.path.join(out_dir, "activities.json"), activities)

    for i, activity in enumerate(activities or [], 1):
        activity_id = activity.get("activityId") or activity.get("id")
        if activity_id is None:
            continue
        print(f" [{i}/{len(activities)}] activity {activity_id}")
        detail = {
            "summary": activity,
            "detail": call("  detail", client.get_activity, activity_id),
            "workouts": call("  workouts", client.get_activity_workouts, activity_id),
        }
        save_json(os.path.join(out_dir, "activities", f"{activity_id}.json"), detail)

        if download_files:
            try:
                raw = client.download_activity(activity_id)
                files_dir = os.path.join(out_dir, "activities", "files")
                os.makedirs(files_dir, exist_ok=True)
                with open(os.path.join(files_dir, f"{activity_id}.zip"), "wb") as f:
                    f.write(raw)
                print("  ok  downloaded original file")
            except Exception as err:
                print(f"  skip download: {err}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=7, help="How many past days of daily metrics to fetch (default: 7)")
    parser.add_argument("--activities-limit", type=int, default=20, help="Max activities to fetch details for (default: 20)")
    parser.add_argument("--download-files", action="store_true", help="Also download the original activity file (zip) for each activity")
    parser.add_argument("--out", default="data", help="Output directory (default: ./data)")
    args = parser.parse_args()

    print("Connecting to Garmin...")
    try:
        client = get_client()
    except Exception as err:
        sys.exit(f"Could not connect: {err}")
    print("Connected.\n")

    end = date.today().isoformat()
    start = (date.today() - timedelta(days=args.days)).isoformat()

    with client:
        export_profile(client, args.out)
        export_trends(client, args.out, start, end)
        export_daily_details(client, args.out, args.days)
        export_activities(client, args.out, args.activities_limit, args.download_files)

    print(f"\nDone. Data saved under {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()
