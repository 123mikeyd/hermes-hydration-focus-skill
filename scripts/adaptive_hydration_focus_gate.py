#!/usr/bin/env python3
"""Adaptive random-feeling hydration/focus reminder gate for Hermes cron.

This script is meant to run frequently as a script-only cron job, e.g. every
5 or 10 minutes. It keeps its own state so Hermes only needs ONE cron job.

Behavior:
- After a sent reminder, reset to a 45-minute interval and 35% send chance.
- At each eligible check, roll the chance.
- If no reminder is sent, increase the chance and shorten the next interval.
- When a reminder finally sends, reset back to the baseline.
- Empty stdout means Hermes sends nothing.

Suggested cron:
  schedule: every 5m
  script: adaptive_hydration_focus_gate.py
  no_agent: true
"""

from __future__ import annotations

import datetime as dt
import json
import os
import random
from pathlib import Path

BASE_INTERVAL_MINUTES = 45.0
MIN_INTERVAL_MINUTES = 10.0
BASE_CHANCE = 0.35
CHANCE_STEP = 0.20
MAX_CHANCE = 0.95
INTERVAL_SHRINK = 0.5
DAY_START_HOUR = 9
DAY_END_HOUR = 20

STATE_PATH = Path(os.environ.get("HYDRATION_FOCUS_STATE", Path.home() / ".hermes/state/hydration_focus_adaptive.json"))

MESSAGES = [
    "Quick reset: sip water, drop your shoulders, pick the next tiny task.",
    "Water check. Also unclench jaw, breathe once, continue with the next step.",
    "Tiny focus reboot: drink water, stretch hands, then do the next 5 minutes.",
    "Hydrate, look away from the screen for 20 seconds, then choose one action.",
    "Posture check: feet down, shoulders loose, water nearby, next task clear.",
    "Hydration goblin tax: 3 sips before the next scroll.",
    "Tiny monk mode: water, breath, one clean action.",
    "Your tabs are breeding. Sip water, close one, choose the next move.",
    "Knightly quest: refill chalice, loosen shoulders, defeat one tiny task.",
    "NASA-grade reset: oxygen, water, trajectory correction. Next 5 minutes only.",
    "Stoic ping: control the sip, control the next step, ignore the circus.",
    "Soft reboot: jaw unclenched, shoulders down, water in system.",
    "Gremlin says: drink water before becoming a raisin with Wi-Fi.",
    "Micro-challenge: 3 sips, 3 breaths, 1 tab closed.",
    "Future-you sent a memo: water now, fewer headaches later.",
]


def now_local() -> dt.datetime:
    return dt.datetime.now().astimezone()


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value)
    except ValueError:
        return None


def iso(value: dt.datetime) -> str:
    return value.isoformat(timespec="seconds")


def default_state(now: dt.datetime) -> dict:
    return {
        "chance": BASE_CHANCE,
        "interval_minutes": BASE_INTERVAL_MINUTES,
        "next_check_after": iso(now + dt.timedelta(minutes=BASE_INTERVAL_MINUTES)),
        "last_sent_at": None,
        "miss_count": 0,
    }


def load_state(now: dt.datetime) -> dict:
    if not STATE_PATH.exists():
        return default_state(now)
    try:
        data = json.loads(STATE_PATH.read_text())
    except (OSError, json.JSONDecodeError):
        return default_state(now)
    state = default_state(now)
    state.update({k: data.get(k, v) for k, v in state.items()})
    return state


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    tmp.replace(STATE_PATH)


def reset_after_send(now: dt.datetime) -> dict:
    return {
        "chance": BASE_CHANCE,
        "interval_minutes": BASE_INTERVAL_MINUTES,
        "next_check_after": iso(now + dt.timedelta(minutes=BASE_INTERVAL_MINUTES)),
        "last_sent_at": iso(now),
        "miss_count": 0,
    }


def increase_after_miss(state: dict, now: dt.datetime) -> dict:
    current_interval = float(state.get("interval_minutes", BASE_INTERVAL_MINUTES))
    current_chance = float(state.get("chance", BASE_CHANCE))
    next_interval = max(MIN_INTERVAL_MINUTES, current_interval * INTERVAL_SHRINK)
    next_chance = min(MAX_CHANCE, current_chance + CHANCE_STEP)
    return {
        **state,
        "chance": next_chance,
        "interval_minutes": next_interval,
        "next_check_after": iso(now + dt.timedelta(minutes=next_interval)),
        "miss_count": int(state.get("miss_count", 0)) + 1,
    }


def main() -> int:
    now = now_local()

    # Do not advance probability/interval during quiet hours.
    if not (DAY_START_HOUR <= now.hour < DAY_END_HOUR):
        return 0

    state = load_state(now)
    next_check = parse_time(state.get("next_check_after"))
    if next_check and now < next_check:
        return 0

    chance = float(state.get("chance", BASE_CHANCE))
    if random.random() <= chance:
        print(random.choice(MESSAGES))
        save_state(reset_after_send(now))
    else:
        save_state(increase_after_miss(state, now))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
