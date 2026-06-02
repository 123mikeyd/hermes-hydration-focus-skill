# Upload instructions

GitHub upload is ready locally, but the agent could not verify GitHub auth in this session.

After you authenticate safely in your own shell:

```bash
gh auth login
cd /home/mikeyd/hermes-hydration-focus-skill
gh repo create hermes-hydration-focus-skill --public --description "Hermes Agent skill for hydration and focus check-ins" --source . --push
```

If the repo already exists:

```bash
cd /home/mikeyd/hermes-hydration-focus-skill
git remote add origin https://github.com/123mikeyd/hermes-hydration-focus-skill.git 2>/dev/null || true
git push -u origin main
```

Suggested X reply after the repo is public:

```text
Yep — made a little Hermes skill for exactly this: hydration/focus check-ins, scheduled or random-feeling, with cron + messaging delivery. Here you go: https://github.com/123mikeyd/hermes-hydration-focus-skill
```
