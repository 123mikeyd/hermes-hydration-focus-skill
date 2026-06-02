#!/usr/bin/env python3
"""Random-feeling hydration/focus reminder gate for Hermes cron.

Use with a script-only Hermes cron job:
  schedule: every 45m
  script: scripts/hydration_focus_gate.py
  no_agent: true

When this script prints a line, Hermes sends it. When it prints nothing,
Hermes stays silent.
"""

import datetime as dt
import random

now = dt.datetime.now()

# Quiet hours: only send during daytime local hours.
if not (9 <= now.hour < 20):
    raise SystemExit(0)

# A 35% chance every 45 minutes averages a few nudges/day.
if random.random() > 0.35:
    raise SystemExit(0)

MESSAGES = [
    "Quick reset: sip water, drop your shoulders, pick the next tiny task.",
    "Water check. Also unclench jaw, breathe once, continue with the next step.",
    "Tiny focus reboot: drink water, stretch hands, then do the next 5 minutes.",
    "Hydrate, look away from the screen for 20 seconds, then choose one action.",
    "Posture check: feet down, shoulders loose, water nearby, next task clear.",
]

print(random.choice(MESSAGES))
