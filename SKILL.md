---
name: hydration-focus-checkins
description: Use when a user wants Hermes to send hydration, stretch, posture, or focus reminders throughout the day using cron jobs, messaging delivery, optional randomized timing, and concise supportive wording.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, cron, reminders, productivity, wellness, messaging]
    related_skills: [hermes-agent]
---

# Hydration and Focus Check-ins

## Overview

This skill helps Hermes set up lightweight hydration and focus nudges for a user. It is designed for people who want the agent to send messages throughout the day like:

- drink water
- stretch or relax shoulders
- check posture
- take a short breathing break
- pick the next concrete task
- avoid drifting into distraction

The safest default is messaging rather than calls. Messages work through Hermes cron delivery to the current chat, Telegram, Discord, Slack, SMS, Matrix, email, or another configured gateway target. Voice or calls depend on the user's configured platform and TTS/calling stack, so treat those as optional upgrades after simple text reminders work.

## When to Use

Use this skill when the user asks for:

- random or scheduled reminders during the day
- hydration reminders
- focus check-ins
- productivity nudges
- wellness nudges that should not be medical advice
- a Hermes cron job that sends short messages to a messaging platform
- a reusable template for reminders that another Hermes user can install

Do not use this skill for:

- medication reminders without explicit safety wording and user review
- emergency, medical, mental-health crisis, or safety-critical alerts
- anything that requires guaranteed delivery
- harassment, nagging, shame-based motivation, or manipulative messaging
- contacting third parties without clear user consent

## Quick Setup: Simple Recurring Reminder

For a basic reminder every 90 minutes, create a cron job like this:

```text
Schedule: every 90m
Prompt: Send me one short supportive hydration and focus check-in. Keep it under 160 characters. Vary the wording. Mention water, posture, stretch, or picking the next concrete task. Do not shame me.
Delivery: origin
```

If the user is in a Hermes session with cron tools available, use the cron job tool directly:

```python
cronjob(
  action="create",
  name="hydration-focus-checkin",
  schedule="every 90m",
  prompt="Send me one short supportive hydration and focus check-in. Keep it under 160 characters. Vary the wording. Mention water, posture, stretch, or picking the next concrete task. Do not shame me.",
)
```

If using the Hermes CLI, use the cron UI:

```bash
hermes cron create 'every 90m'
```

Then paste the prompt above when asked.

## Recommended Reminder Prompt

Use this as the default cron prompt:

```text
You are sending a brief hydration/focus check-in to the user.

Constraints:
- Under 160 characters.
- Friendly, casual, and non-shaming.
- Vary the wording each time.
- Choose one or two themes: water, stretch, posture, eye break, breathing, or choosing the next concrete task.
- Do not mention that you are an AI unless useful.
- Do not over-explain.

Examples of acceptable style:
- Quick reset: sip some water, drop your shoulders, and pick the next tiny task.
- Water check. Also: unclench jaw, breathe once, continue with the next concrete step.
- Tiny focus reboot: drink water, stretch your hands, then do the next 5 minutes.
```

## Randomized Timing Pattern

Hermes cron schedules are deterministic. To create a more random-feeling reminder pattern, use a frequent cron job with a small script that sometimes stays quiet. This is best for users who want "randomly throughout the day" without being spammed.

Create a script at `~/.hermes/scripts/hydration_focus_gate.py`:

```python
#!/usr/bin/env python3
import datetime as dt
import random

now = dt.datetime.now()

# Only send during daytime local hours.
if not (9 <= now.hour < 20):
    raise SystemExit(0)

# Do not send every tick. A 35% chance every 45 minutes averages a few nudges/day.
if random.random() > 0.35:
    raise SystemExit(0)

messages = [
    "Quick reset: sip water, drop your shoulders, pick the next tiny task.",
    "Water check. Also unclench jaw, breathe once, continue with the next step.",
    "Tiny focus reboot: drink water, stretch hands, then do the next 5 minutes.",
    "Hydrate, look away from the screen for 20 seconds, then choose one action.",
    "Posture check: feet down, shoulders loose, water nearby, next task clear.",
]

print(random.choice(messages))
```

Then create a script-only cron job:

```python
cronjob(
  action="create",
  name="random-hydration-focus-checkin",
  schedule="every 45m",
  script="hydration_focus_gate.py",
  no_agent=True,
)
```

Important behavior: with `no_agent=True`, empty stdout means Hermes sends nothing. This lets the script decide whether a check-in happens.

## Delivery Targets

Default delivery should be the origin conversation unless the user asks otherwise. If the user asks for a specific channel or person, list available targets first and choose the exact target.

Common delivery values:

- omit `deliver` or use `origin` for the current chat/thread
- `telegram` for the default Telegram home channel
- `discord:#channel-name` for a specific Discord channel when available
- `sms:+15551234567` for SMS when configured
- `email` or a specific email workflow when configured

Do not use WhatsApp if the user has said not to use WhatsApp.

## Voice and Calls

Text reminders are the reliable default. If the user asks for voice:

1. Check whether Hermes TTS is configured.
2. Check whether the target platform supports native audio delivery.
3. Start with a short test message.
4. Avoid recurring voice reminders until the user confirms the volume, voice, and cadence are acceptable.

A voice reminder can be generated with TTS in a normal Hermes run, but cron delivery support depends on the platform. Do not promise phone calls unless a calling integration is actually configured and tested.

## Tone Guidelines

Good reminder tone:

- short
- warm
- useful
- specific
- non-judgmental
- varied

Avoid:

- guilt trips
- productivity bro language
- medical claims
- long lectures
- pretending delivery is guaranteed
- messages that interrupt too often

## Example Message Bank

```text
Quick reset: sip some water, drop your shoulders, and pick the next tiny task.
Water check. Also: unclench jaw, breathe once, continue with the next concrete step.
Tiny focus reboot: drink water, stretch your hands, then do the next 5 minutes.
Hydrate and look 20 feet away for 20 seconds. Then return to one clear action.
Posture check: shoulders loose, water nearby, next task obvious.
Small reset: water, breath, stretch, then one doable step.
Refill if needed. Future-you likes having water within reach.
Take one sip and close one distraction tab if you can.
Hydration ping: water first, then the next thing on purpose.
Pause for ten seconds. Water, shoulders, next tiny task.
```

## Example Full Cron Job

```python
cronjob(
  action="create",
  name="daytime-hydration-focus",
  schedule="every 2h",
  repeat=None,
  prompt="""
Send the user a short hydration/focus check-in.
Keep it under 160 characters.
Be warm, casual, and non-shaming.
Choose one or two: water, posture, stretch, breathing, eye break, or next concrete task.
Vary the wording. Do not include medical advice.
""".strip(),
)
```

## Common Pitfalls

1. Creating reminders that are too frequent. Start with every 90 minutes or every 2 hours, then adjust after user feedback.

2. Calling deterministic cron "random." If the user wants random-feeling timing, use the script-gate pattern that sometimes prints nothing.

3. Overusing TTS. Voice reminders can become annoying quickly. Test once before scheduling repeated audio.

4. Forgetting quiet hours. Do not send wellness nudges overnight unless the user explicitly asks.

5. Treating reminders as medical or safety-critical. Hermes cron is useful, but it is not a guaranteed medical alert system.

6. Sending to the wrong channel. When a user names a specific channel or person, list targets first instead of guessing.

## Verification Checklist

- [ ] The reminder cadence is clear.
- [ ] Quiet hours are considered.
- [ ] Delivery target is correct.
- [ ] Wording is short and non-shaming.
- [ ] The user understands that delivery is not safety-critical guaranteed delivery.
- [ ] For random-feeling reminders, the script sometimes exits silently.
- [ ] For voice reminders, a one-off audio test succeeded before scheduling repeats.
