# Build a badge app with Copilot

Use this page for the shortest path from an idea to a tested app.

## 1. Set up the repository

Use Python 3.10 or newer (only the standard library is required -- no
`pip install` needed).

## 2. Update your team fork and create a branch

Your shared team fork uses `origin`. This repository uses `upstream`.
Replace `team1` with your assigned team number and choose a short app name:

```bash
git switch main
git fetch upstream
git merge --ff-only upstream/main
git switch -c team1/countdown
```

Do not build directly on `main`.

## 3. Give Copilot one complete prompt

Open this repository in your Copilot-enabled editor or terminal. Replace the
team, app name, idea, and controls in this prompt:

```text
I am on Team 1. Build a badge app in Team1/countdown.

The app should show a countdown to a date. A and C change the date. B saves
the choice. The choice must still be there after I close and reopen the app.

Use the badge-app-builder skill and inspect the closest examples in
badge/apps before writing code. Do not change badge/apps because those are
shared examples. Create a 24x24 icon, validate the app, and tell me what I
must test in the Pimoroni Badgeware Web Simulator and on a physical badge.
```

Good prompts tell Copilot:

- Your assigned `TeamN` folder.
- The exact app folder name.
- What the app should do.
- What each button should do.
- What data must be saved.
- Whether the app needs Wi-Fi, BLE, IR, LEDs, or another hardware feature.

## 4. Run the app

Copilot should run the validator. You can also run it yourself:

```bash
python3 .github/skills/badge-app-builder/scripts/validate_app.py \
  Team1/countdown
```

Test the app in the
[Pimoroni Badgeware Web Simulator](https://pimoroni.github.io/badgeware-web-simulator/):

- Use A, B, C, and the arrow keys to test every control.
- Reload after a code change to test the updated app.
- Check that HOME returns to the launcher.
- Test a fresh load to check the first-use experience.

The web simulator cannot prove that BLE, GPIO, physical IR, LEDs, battery
behavior, radio behavior, or exact badge performance works.

## 5. Ask Copilot to check the finished work

```text
Review Team1/countdown as a badge submission. Fix validation errors, test every
screen and control in the Pimoroni Badgeware Web Simulator, check for secrets
and generated files, and list anything that still needs a physical badge test.
Do not edit files outside Team1/countdown unless a shared tool is broken.
```

Check every app in the team folder:

```bash
python3 .github/skills/badge-app-builder/scripts/validate_submissions.py Team1
```

## 6. Open a pull request

Commit only your team's work, push the branch, and open a pull request into the
shared fork's `main` branch. The pull request template asks for the app list,
controls, completed checks, and remaining hardware tests.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full shared-fork workflow.
