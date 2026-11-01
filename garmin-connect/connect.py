#!/usr/bin/env python3
"""Verify your Garmin Connect personal API key works.

This uses Garmin's own official Personal API client, not a reverse-engineered
login. Create a key at Garmin Connect -> Settings -> "Chave de API pessoal"
(or https://connect.garmin.com/app/settings/personalApiToken), then run this
on your OWN machine, in your own terminal:

    python3 connect.py

It asks for the key right here in the terminal (hidden input via getpass, so
it's never echoed to the screen and never leaves this script — it goes
straight to Garmin's servers) unless GARMIN_PERSONAL_API_KEY is already set
as an environment variable.
"""

import os
import sys
from getpass import getpass

try:
    from garmin_personal_api import GarminPersonalApiClient, PersonalApiAuthenticator
except ImportError:
    sys.exit(
        "garmin-connect-personal-api-python is not installed.\n"
        "Run: pip install -r requirements.txt"
    )


def main() -> None:
    api_key = os.getenv("GARMIN_PERSONAL_API_KEY") or getpass("Garmin personal API key: ")

    print("Connecting to Garmin...")
    try:
        with PersonalApiAuthenticator() as authenticator:
            token = authenticator.obtain_token(api_key)
        with GarminPersonalApiClient(token.access_token) as client:
            profile = client.get_user_profile_settings()
    except Exception as err:
        sys.exit(f"Could not connect: {err}")

    print("\nConnected.")
    if isinstance(profile, dict):
        name = profile.get("displayName") or profile.get("firstName")
        if name:
            print(f"Garmin profile: {name}")


if __name__ == "__main__":
    main()
