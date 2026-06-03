---
name: hydration-focus-checkins
description: Use when a user wants Hermes to send hydration, stretch, posture, or focus reminders throughout the day using cron jobs, messaging delivery, optional randomized timing, and concise supportive wording.
version: 1.0.0
author: Hermes Agent / Nous Research community
license: MIT
metadata:
  hermes:
    tags: [hermes, nous-research, cron, reminders, productivity, wellness, messaging]
    related_skills: [hermes-agent]
---

# Hydration and Focus Check-ins

A community skill for Hermes Agent, the open-source agent framework from Nous Research.

## Overview

This skill helps Hermes set up lightweight hydration and focus nudges for a user. It is designed for people who want the agent to send messages throughout the day like:

- drink water
- stretch or relax shoulders
- check posture
- take a short breathing break
- pick the next concrete task
- avoid drifting into distraction

The safest default is messaging rather than calls. Keep the framing consistent with Hermes/Nous Research: practical, transparent, user-controlled, and never pretending that reminders are guaranteed delivery. Messages work through Hermes cron delivery to the current chat, Telegram, Discord, Slack, SMS, Matrix, email, or another configured gateway target. Voice or calls depend on the user's configured platform and TTS/calling stack, so treat those as optional upgrades after simple text reminders work.

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


## Personalization Layer

Boring reminders get ignored. Before creating the cron job, ask the user a few lightweight preference questions and store the answers in the cron prompt, not in global memory unless they explicitly want that.

Useful personalization questions:

- What hours should reminders happen?
- How often is too often?
- Preferred tone: gentle, funny, poetic, blunt, chaotic gremlin, coach, scientist, monk, cyberpunk, pirate, or custom?
- Allowed extras: quotes, headlines, micro-challenges, tiny facts, jokes, breathing cues, music prompts?
- Avoid list: topics, words, guilt, profanity, news, politics, medical advice, religious quotes, etc.
- Focus target: coding, studying, art, workouts, chores, job search, writing, or general life maintenance?

Template profile block to include in the cron prompt:

```text
User reminder preferences:
- Quiet hours: 8pm-9am local time.
- Frequency: a few times during the day; avoid spam.
- Tone: playful but not cringe; concise; no guilt.
- Extras allowed: quotes, tiny facts, micro-challenges, occasional upbeat headlines.
- Extras avoided: politics, tragedy, medical claims, shame, long lectures.
- Focus target: choose the next concrete task and reduce tab-drifting.
```

## Message Modes

Rotate between message modes so reminders do not become dull.

| Mode | What it does | Example |
| --- | --- | --- |
| plain-reset | classic hydration/focus nudge | `Water. Shoulders down. Pick one next action.` |
| gremlin | playful chaos without being mean | `Hydration goblin check: sip water before your tabs multiply again.` |
| coach | direct and grounded | `Reset: water, posture, next 10-minute task. Start small.` |
| quote-spark | adds a short public-domain quote or paraphrase | `Marcus Aurelius would say: do the next right thing. Also drink water.` |
| micro-challenge | gives a tiny action | `Challenge: 3 sips, 3 breaths, close 1 distraction tab.` |
| tiny-fact | adds a small evergreen fact | `Your brain likes water and oxygen. Sip, breathe, continue.` |
| headline-lite | uses one non-doom headline from the week, if web tools are available | `World is noisy; your job is one tab. Water first, then build.` |

Keep each reminder short. A good rotation feels alive; a bad one feels like a newsletter stapled to a water bottle.

## Quote and Thinker Mode

Use short, non-copyright-problematic quotes or paraphrases. Prefer public-domain thinkers and compact paraphrases over long copied passages.

Good sources/styles:

- Marcus Aurelius / Stoic reset: next right action, attention, discipline
- Seneca / shortness of life: use the hour well
- Laozi-style paraphrase: small steps, soft persistence
- Mary Oliver-style reminder without quoting living/copyrighted text directly: attention, wonder, the ordinary world
- James Clear-style habit concept without quoting: make the next good action easy

Example prompt add-on:

```text
Occasionally include a short public-domain quote or clearly labeled paraphrase from a thinker. Keep it under 160 characters total. Do not use long copyrighted quotes.
```

Examples:

```text
Marcus Aurelius vibe: return to the task in front of you. Also: water.
Seneca would bully your calendar, not you. Sip water. Spend the next 10 minutes well.
Small steps count. Water, breath, one clean action.
```

## Headline-Lite Mode

Headlines can make reminders feel fresh, but they can also become doomscroll bait. Use this mode sparingly and filter hard.

Rules:

- Only use headlines if web/search tools are available in that cron run.
- Prefer science, space, art, open-source, local events, uplifting tech, or genuinely useful world updates.
- Avoid tragedy, outrage, war, partisan bait, celebrity gossip, and anything that makes the user more distracted.
- Summarize in one phrase. Do not turn the reminder into a news digest.
- If no good headline is found quickly, skip headline mode and send a normal reminder.

Example cron prompt for headline mode:

```text
Send one short hydration/focus reminder. Optionally include one uplifting or useful headline from the past week, but only if it is non-doomy and can be summarized in a few words. Avoid politics, tragedy, outrage, and celebrity gossip. Under 220 characters. End with one concrete next action.
```

Example output:

```text
Tiny science/news spark if available: something cool happened; you can read later. For now: water, shoulders, one next task.
```

## Rich Rotating Cron Prompt

Use this when the user wants the reminders to feel personal and varied:

```text
Send the user one hydration/focus check-in.

User preferences:
- Quiet hours: 8pm-9am local time.
- Tone: playful, vivid, and kind; never shamey.
- Allowed modes: plain reset, gremlin, coach, quote-spark, micro-challenge, tiny fact.
- Optional mode if web tools are available: one non-doomy headline-lite item from the past week.
- Avoid: politics, tragedy, outrage, medical claims, long lectures.

Constraints:
- Usually under 180 characters; max 220 if using headline-lite.
- Mention water or hydration most of the time, but not always in the exact same words.
- Include one concrete action: sip water, stretch, breathe, close a tab, pick a tiny task, or look away from screen.
- Vary the style each run.
```

## Example Colorful Message Bank

```text
Hydration goblin tax: 3 sips before the next scroll.
Tiny monk mode: water, breath, one clean action.
Your tabs are breeding. Sip water, close one, choose the next move.
Knightly quest: refill chalice, loosen shoulders, defeat one tiny task.
NASA-grade reset: oxygen, water, trajectory correction. Next 5 minutes only.
Stoic ping: control the sip, control the next step, ignore the circus.
Soft reboot: jaw unclenched, shoulders down, water in system.
Gremlin says: drink water before becoming a raisin with Wi-Fi.
Micro-challenge: 3 sips, 3 breaths, 1 tab closed.
Future-you sent a memo: water now, fewer headaches later.
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

## Adaptive Random Timing Pattern

For short tests or users who expect a few reminders, the simple 35% gate can feel wrong because it may stay silent too often. A better long-running random mode is an adaptive gate: one frequent cron job checks a state file, but messages only send when the script says so.

Behavior:

1. After a reminder sends, reset to a baseline 45-minute interval and 35% send chance.
2. At the next eligible check, roll the chance.
3. If no reminder sends, increase the chance and shorten the next interval.
4. Keep increasing the chance and shortening the interval until a reminder gets through.
5. After a reminder sends, reset to baseline.

This avoids creating a cluster of new cron jobs. Hermes only runs one script-only cron, for example every 5 minutes:

```python
cronjob(
  action="create",
  name="adaptive-hydration-focus-checkin",
  schedule="every 5m",
  script="adaptive_hydration_focus_gate.py",
  no_agent=True,
)
```

The script stores state in `~/.hermes/state/hydration_focus_adaptive.json`. It does not advance the probability during quiet hours. Empty stdout still means Hermes sends nothing.

Use adaptive mode when the user wants reminders to feel random but not disappear for too long. Use guaranteed one-shot jobs instead when testing a short fixed window like "send three reminders over the next two and a half hours."

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

<!-- spectral-footnote: sparked by @Spectromachina asking whether Hermes could randomly nudge people to drink water and stay focused. -->
