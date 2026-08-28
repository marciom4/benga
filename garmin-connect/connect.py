#!/usr/bin/env python3
"""Connect this computer to your Garmin Connect account.

Run this on your OWN machine, in your own terminal:

    python3 connect.py

It asks for your Garmin email/password right here in the terminal
(the password uses getpass, so it is never echoed to the screen and
never leaves this script — it goes straight to Garmin's servers).
After a successful login, a session token is cached at
~/.garminconnect so you won't have to log in again on this machine.
"""

import os
import sys
from datetime import date
from getpass import getpass

try:
    from garminconnect import (
        Garmin,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
    )
except ImportError:
    sys.exit(
        "garminconnect is not installed.\n"
        "Run: pip install -r requirements.txt"
    )

TOKEN_STORE = os.path.expanduser("~/.garminconnect")


def prompt_mfa() -> str:
    return input("Garmin sent a code to your email/phone. Enter it here: ").strip()


def login() -> Garmin:
    email = os.getenv("GARMIN_EMAIL") or input("Garmin email: ").strip()
    password = os.getenv("GARMIN_PASSWORD") or getpass("Garmin password: ")

    client = Garmin(email, password, prompt_mfa=prompt_mfa)
    client.login(TOKEN_STORE)
    return client


def main() -> None:
    print("Connecting to Garmin Connect...")
    try:
        client = login()
    except GarminConnectAuthenticationError:
        sys.exit("Login failed: wrong email/password or MFA code.")
    except GarminConnectTooManyRequestsError:
        sys.exit("Too many login attempts. Wait a while and try again.")
    except GarminConnectConnectionError as err:
        sys.exit(f"Could not reach Garmin Connect: {err}")

    profile = client.get_full_name()
    print(f"\nConnected as {profile}.")
    print(f"Session cached at {TOKEN_STORE} — next runs won't ask for your password again.")

    today = date.today().isoformat()
    try:
        stats = client.get_stats(today)
        steps = stats.get("totalSteps")
        if steps is not None:
            print(f"Steps today: {steps}")
    except Exception:
        # Stats are just a sanity check; a failure here doesn't mean the
        # connection itself failed.
        pass


if __name__ == "__main__":
    main()
