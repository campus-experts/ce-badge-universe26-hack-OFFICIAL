from badgeware import State

STATE_PET = 0
STATE_HEATMAP = 1

BUTTON_LEFT = BUTTON_LEFT if "BUTTON_LEFT" in globals() else BUTTON_A
BUTTON_RIGHT = BUTTON_RIGHT if "BUTTON_RIGHT" in globals() else BUTTON_C
BUTTON_SELECT = BUTTON_SELECT if "BUTTON_SELECT" in globals() else BUTTON_B

MOOD_REST = 0
MOOD_ACTIVE = 1
MOOD_FLOW = 2
MOOD_LABELS = ["Resting Zzz", "Building!", "In Flow!"]

state = STATE_PET
commits = 42
streak = 2
level = 4
xp = 15
MAX_XP = 100
tick_ms = 0
levelup_ms = 0
idle_ms = 0
mood = MOOD_FLOW

# 7 rows x 16 weeks of commit levels (0-3)
grid = [
    [1, 2, 0, 3, 1, 0, 2, 3, 0, 1, 2, 3, 1, 0, 2, 1],
    [0, 1, 3, 2, 0, 1, 1, 2, 3, 0, 1, 2, 0, 3, 1, 2],
    [2, 0, 1, 1, 3, 2, 0, 1, 2, 3, 0, 1, 2, 1, 0, 3],
    [1, 3, 2, 0, 1, 2, 3, 1, 0, 2, 1, 3, 2, 0, 1, 1],
    [0, 2, 1, 3, 0, 1, 2, 0, 3, 1, 2, 0, 1, 3, 2, 0],
    [3, 1, 0, 2, 2, 3, 1, 0, 1, 2, 3, 1, 0, 2, 1, 2],
    [1, 0, 2, 1, 1, 0, 3, 2, 0, 1, 2, 3, 1, 0, 3, 1],
]

saved = {"commits": commits, "streak": streak, "level": level, "xp": xp, "grid": grid}
State.load("octotchi", saved)
commits = saved["commits"]
streak = saved["streak"]
level = saved["level"]
xp = saved["xp"]
grid = saved["grid"]

screen.font = font.absolute

BG = color.rgb(13, 17, 23)
TEXT = color.rgb(240, 240, 240)
ACCENT = color.rgb(88, 166, 255)
YELLOW = color.rgb(241, 196, 15)
HEAT = [
    color.rgb(22, 27, 34),
    color.rgb(14, 68, 41),
    color.rgb(0, 109, 50),
    color.rgb(38, 166, 65),
]


def rect(x, y, w, h, pen):
    screen.pen = pen
    screen.shape(shape.rectangle(x, y, w, h))


def eval_mood():
    global mood
    if streak >= 7 or xp >= 70:
        mood = MOOD_FLOW
    elif xp < 30:
        mood = MOOD_REST
    else:
        mood = MOOD_ACTIVE


def add_commit():
    global commits, xp, level, streak, levelup_ms
    commits += 1
    xp += 20
    if xp >= MAX_XP:
        level += 1
        xp -= MAX_XP
        streak += 1
        levelup_ms = 1200
    grid[6][15] = min(3, grid[6][15] + 1)
    saved.update(commits=commits, streak=streak, level=level, xp=xp, grid=grid)
    State.save("octotchi", saved)


def draw_pet():
    screen.pen = YELLOW if levelup_ms > 0 else TEXT
    screen.text("LEVEL UP!" if levelup_ms > 0 else "OCTOTCHI", 4, 4)
    screen.text("Lv.%d" % level, screen.width - 36, 4)

    if mood == MOOD_FLOW:
        bounce = 3 if (tick_ms // 130) % 2 == 0 else 0
    elif mood == MOOD_ACTIVE:
        bounce = 2 if (tick_ms // 250) % 2 == 0 else 0
    else:
        bounce = 1 if (tick_ms // 500) % 2 == 0 else 0

    sx, sy = 12, 32 + bounce
    rect(sx + 8, sy, 24, 24, ACCENT)
    rect(sx, sy + 4, 8, 8, ACCENT)
    rect(sx + 32, sy + 4, 8, 8, ACCENT)

    if mood == MOOD_FLOW:
        rect(sx + 8, sy + 6, 24, 8, BG)
        rect(sx + 10, sy + 8, 8, 4, YELLOW)
        rect(sx + 22, sy + 8, 8, 4, YELLOW)
        rect(sx + 14, sy + 18, 12, 3, BG)
    elif mood == MOOD_ACTIVE:
        rect(sx + 12, sy + 8, 4, 6, BG)
        rect(sx + 24, sy + 8, 4, 6, BG)
        rect(sx + 16, sy + 18, 8, 2, BG)
    else:
        rect(sx + 11, sy + 10, 6, 2, BG)
        rect(sx + 23, sy + 10, 6, 2, BG)
        rect(sx + 17, sy + 17, 6, 2, BG)

    screen.pen = TEXT
    screen.text("Commits: %d" % commits, 62, 28)
    screen.text("Streak: %dd" % streak, 62, 40)
    screen.pen = YELLOW if mood == MOOD_FLOW else TEXT
    screen.text(MOOD_LABELS[mood], 62, 52)

    screen.pen = TEXT
    screen.text("XP", 4, 72)
    rect(24, 72, 100, 8, ACCENT)
    rect(26, 74, int(xp * 96 / MAX_XP), 4, HEAT[3])

    screen.pen = TEXT
    screen.text("UP:Commit  L/R:Graph", 4, screen.height - 14)


def draw_heatmap():
    screen.pen = TEXT
    screen.text("CONTRIBUTIONS", 4, 4)
    for row in range(7):
        for col in range(16):
            rect(12 + col * 8, 22 + row * 8, 6, 6, HEAT[grid[row][col]])
    screen.pen = TEXT
    screen.text("Total: %d commits" % commits, 4, 84)
    screen.text("UP:+1  BACK/L/R:Pet", 4, screen.height - 14)


def update():
    global state, tick_ms, levelup_ms, idle_ms, xp
    tick_ms = (tick_ms + badge.ticks_delta) % 1000000
    levelup_ms = max(0, levelup_ms - badge.ticks_delta)

    view_pressed = badge.pressed(BUTTON_LEFT) or badge.pressed(BUTTON_RIGHT)
    commit_pressed = badge.pressed(BUTTON_SELECT) or badge.pressed(BUTTON_UP)
    back_pressed = "BUTTON_BACK" in globals() and badge.pressed(BUTTON_BACK)
    if view_pressed or commit_pressed or back_pressed:
        idle_ms = 0
    else:
        idle_ms += badge.ticks_delta

    if idle_ms >= 3000:
        idle_ms -= 3000
        new_xp = max(0, xp - 5)
        if new_xp != xp:
            xp = new_xp
            saved["xp"] = xp
            State.save("octotchi", saved)

    if back_pressed and state == STATE_HEATMAP:
        state = STATE_PET
    elif view_pressed:
        state = STATE_HEATMAP if state == STATE_PET else STATE_PET
    if commit_pressed:
        add_commit()
    eval_mood()

    rect(0, 0, screen.width, screen.height, BG)
    if state == STATE_PET:
        draw_pet()
    else:
        draw_heatmap()


run(update)
