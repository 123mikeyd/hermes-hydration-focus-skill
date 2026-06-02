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
    # plain reset
    "Quick reset: sip water, drop your shoulders, pick the next tiny task.",
    "Water check. Also unclench jaw, breathe once, continue with the next step.",
    "Tiny focus reboot: drink water, stretch hands, then do the next 5 minutes.",
    "Hydrate, look away from the screen for 20 seconds, then choose one action.",
    "Posture check: feet down, shoulders loose, water nearby, next task clear.",

    # more colorful modes
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

print(random.choice(MESSAGES))
