# Universe 2026 emulator workflow

Use the [Pimoroni Badgeware Web Simulator](https://pimoroni.github.io/badgeware-web-simulator/)
for a quick visual check of an app. It runs in a browser with no install and
models the 2026 runtime for UI and state iteration. It does not prove
physical touch, IMU, wireless, GPIO, IR, power, or exact MicroPython memory
behavior.

## Setup

No local install is required. Open
https://pimoroni.github.io/badgeware-web-simulator/ and load the app's
`__init__.py` (and any local modules or assets).

If you want offline or command-line testing instead, see
[`pimoroni/badgeware-simulator`](https://github.com/pimoroni/badgeware-simulator),
a native simulator Pimoroni builds directly on the real PicoVector graphics
library.

## Controls

Use the simulator's logical controls, which follow the physical badge's
layout:

- Arrow keys or on-screen buttons: directional actions.
- Enter/select: SELECT.
- Back/escape: BACK.
- Menu: MENU.
- Home: return to the launcher.

The exact controls are shown in the simulator UI and may change as the 2026
input model gains touch and orientation support.

## What to test

Exercise every screen, logical control, launcher return path, first-run state
path, saved-state path, and error path.

Do not mark BLE, touch, IMU, GPIO, IR, battery, charging, wireless, or exact
memory behavior as complete from simulator success alone.
