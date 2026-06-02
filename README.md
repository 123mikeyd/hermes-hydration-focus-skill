# Hermes Hydration + Focus Check-ins Skill

A small reusable Hermes Agent skill for setting up hydration, stretch, posture, and focus reminders throughout the day.

It covers:

- simple recurring reminders with Hermes cron
- random-feeling check-ins using a script gate
- safe delivery defaults
- optional voice/TTS notes
- short non-shaming reminder copy

## Install

Copy or clone this repo into your Hermes skills directory:

```bash
mkdir -p ~/.hermes/skills/productivity
cd ~/.hermes/skills/productivity
git clone https://github.com/123mikeyd/hermes-hydration-focus-skill.git hydration-focus-checkins
```

Then start a new Hermes session and load it:

```bash
hermes -s hydration-focus-checkins
```

Or inside Hermes:

```text
/skill hydration-focus-checkins
```

## Quick cron example

Create a reminder every 90 minutes:

```text
Schedule: every 90m
Prompt: Send me one short supportive hydration and focus check-in. Keep it under 160 characters. Vary the wording. Mention water, posture, stretch, or picking the next concrete task. Do not shame me.
Delivery: origin
```

## Random-feeling reminders

The skill includes a pattern for running every 45 minutes but only sending sometimes, so reminders feel more natural and do not spam you.

## Notes

Hermes cron reminders are useful nudges, not guaranteed safety-critical alerts. For medical, emergency, or medication reminders, use purpose-built systems and review all wording/settings yourself.

## License

MIT
