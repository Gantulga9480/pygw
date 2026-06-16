# Survivors config

# Display
SCREEN_W = 960
SCREEN_H = 600
FPS = 60

# Colors
C_BG = (18, 18, 30)
C_GRID = (28, 28, 45)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_RED = (220, 50, 50)
C_GREEN = (50, 200, 80)
C_YELLOW = (240, 220, 50)
C_PURPLE = (160, 100, 240)
C_CYAN = (60, 220, 220)
C_ORANGE = (240, 140, 40)
C_GOLD = (240, 200, 60)
C_GRAY = (80, 80, 100)
C_DARK_GRAY = (40, 40, 55)
C_LIGHT_GRAY = (160, 160, 180)
C_HP_BAR_BG = (60, 20, 20)
C_XP_BAR_BG = (40, 20, 60)

# Hero colors (primary, secondary)
HERO_ROGUE = ((40, 180, 220), (80, 240, 240))
HERO_WARRIOR = ((220, 60, 60), (240, 180, 40))
HERO_WITCH = ((160, 100, 240), (200, 160, 255))
HERO_ASSASSIN = ((60, 60, 80), (180, 60, 200))

# Enemy colors
C_ENEMY_ZOMBIE = (80, 180, 60)
C_ENEMY_RUNNER = (220, 220, 40)
C_ENEMY_BRUTE = (200, 40, 40)
C_ENEMY_BOSS = (160, 60, 200)

# UI
UI_BAR_HEIGHT = 14
UI_HP_MAX_W = 200
UI_XP_MAX_W = 320
UI_FONT_SIZE = 16
UI_FONT_BIG = 28
UI_FONT_TINY = 12

# HUD layout
HUD_HP_X = 16
HUD_HP_Y = 16
HUD_XP_X = (SCREEN_W - UI_XP_MAX_W) // 2
HUD_XP_Y = 16
HUD_STATS_X = SCREEN_W - 200
HUD_STATS_Y = 16

# Ability icon layout (bottom center)
AB_ICON_SIZE = 40
AB_ICON_PAD = 8
AB_ICON_Y = SCREEN_H - AB_ICON_SIZE - 16


def ab_icon_x(idx):
    """X position for ability icon at index (0-based, centered at bottom)."""
    total_w = AB_ICON_SIZE * 3 + AB_ICON_PAD * 2
    start_x = (SCREEN_W - total_w) // 2
    return start_x + idx * (AB_ICON_SIZE + AB_ICON_PAD)


# Grid
GRID_SPACING = 48


# ---- Enemy Balancing ----
# Spawn
SPAWN_BASE_INTERVAL = 2.0
SPAWN_MIN_INTERVAL = 0.3
SPAWN_INTERVAL_RAMP_TIME = 300  # seconds to reach min interval
BOSS_INTERVAL = 120  # seconds between bosses

# Difficulty scaling
HP_SCALE_PER_MIN = 0.10
DMG_SCALE_PER_MIN = 0.05

# Enemy templates: (hp, speed_px_s, dmg, color, size, outline)
ENEMY_ZOMBIE = dict(hp=30, speed=55, dmg=5, color=C_ENEMY_ZOMBIE, size=(16, 20), outline=C_BLACK)
ENEMY_RUNNER = dict(hp=15, speed=140, dmg=3, color=C_ENEMY_RUNNER, size=(12, 16), outline=C_BLACK)
ENEMY_BRUTE = dict(hp=100, speed=35, dmg=15, color=C_ENEMY_BRUTE, size=(24, 28), outline=C_BLACK)
ENEMY_BOSS = dict(hp=500, speed=45, dmg=25, color=C_ENEMY_BOSS, size=(40, 44), outline=C_GOLD)

# Spawn weights (time_in_minutes -> type)
ENEMY_UNLOCK_RUNNER = 60  # seconds
ENEMY_UNLOCK_BRUTE = 120  # seconds


# ---- Hero Balancing ----
HERO_ROGUE_STATS = dict(
    name="Speed Rogue",
    hp=100,
    speed=240,
    size=(14, 18),
    colors=HERO_ROGUE,
    # Auto-attack ability
    slash=dict(dmg=15, cooldown=1.0, range=180, proj_speed=500, proj_size=6, color=C_CYAN),
    # Q ability
    dash=dict(dmg=0, cooldown=5.0, range=200, duration=0.15, color=C_CYAN),
    # E ability
    poison=dict(dmg=2, cooldown=8.0, duration=3.0, hits=3, color=(80, 220, 100)),
)

HERO_WARRIOR_STATS = dict(
    name="Tank Warrior",
    hp=200,
    speed=150,
    size=(18, 22),
    colors=HERO_WARRIOR,
    # Auto-attack ability
    slam=dict(dmg=20, cooldown=1.5, range=100, proj_speed=0, proj_size=0, color=C_ORANGE),
    # Q ability
    iron_skin=dict(dmg=0, cooldown=8.0, duration=4.0, reduction=0.5, color=C_GOLD),
    # E ability
    rally=dict(dmg=0, cooldown=12.0, duration=3.0, heal=40, color=C_GREEN),
)

HERO_WITCH_STATS = dict(
    name="Frost Witch",
    hp=120,
    speed=130,
    size=(16, 20),
    colors=HERO_WITCH,
    # Auto-attack ability
    frost_bolt=dict(dmg=12, cooldown=1.2, range=200, proj_speed=400, proj_size=8, color=(140, 200, 255)),
    # Q ability
    blizzard=dict(dmg=3, cooldown=10.0, duration=3.0, radius=120, color=(140, 200, 255)),
    # E ability
    ice_nova=dict(dmg=25, cooldown=6.0, range=100, color=(100, 180, 255)),
)

HERO_ASSASSIN_STATS = dict(
    name="Shadow Assassin",
    hp=90,
    speed=200,
    size=(14, 18),
    colors=HERO_ASSASSIN,
    # Auto-attack ability
    shadow_bolt=dict(dmg=18, cooldown=1.0, range=250, proj_speed=350, proj_size=6, color=(140, 80, 180)),
    # Q ability
    shadow_step=dict(dmg=30, cooldown=5.0, range=180, color=(80, 40, 140)),
    # E ability
    shadow_clone=dict(dmg=0, cooldown=15.0, duration=8.0, clone_dmg=0.7, color=(100, 60, 160)),
)


# ---- XP / Leveling ----
XP_BASE = 20
XP_SCALE = 1.5  # xp_to_next = XP_BASE * XP_SCALE ** (level - 1)
LEVEL_UP_MAX = 50

# XP gem
GEM_SIZE = 8
GEM_COLORS = [(120, 60, 220), (180, 100, 255), (100, 220, 240)]
GEM_VALUES = [1, 3, 5]

# Magnet range (gems auto-collect within this range)
MAGNET_RANGE = 120


# ---- Effects ----
DAMAGE_NUMBER_LIFETIME = 1.0
DAMAGE_NUMBER_RISE_SPEED = 60
PARTICLE_LIFETIME = 0.6
PARTICLE_COUNT_DEATH = 8
PARTICLE_COUNT_HIT = 3
FLASH_DURATION = 0.1


# ---- Sound ----
SFX_CHANNELS = 4

# ---- Upgrade System ----
UPGRADE_CARD_W = 200
UPGRADE_CARD_H = 140
UPGRADE_CARD_PAD = 16
UPGRADE_CARD_RADIUS = 8

RARITY_COLORS = {
    "common": (160, 160, 180),
    "uncommon": (50, 200, 80),
    "rare": (160, 100, 240),
}
RARITY_BORDERS = {
    "common": (100, 100, 120),
    "uncommon": (80, 180, 100),
    "rare": (160, 100, 240),
}


def _apply_stat(hero, stats, key, value):
    hero.upgrade_data[key] = hero.upgrade_data.get(key, 0) + value


def _apply_pct(hero, stats, key, value):
    hero.upgrade_data[key] = hero.upgrade_data.get(key, 0) + value


def _apply_weapon(hero, stats, weapon):
    hero.unlocked_weapons.append(weapon)


UPGRADES = [
    # ===== GLOBAL — available to both heroes =====
    dict(name="Vitality", desc="+10 Max HP", rarity="common", weight=3,
         global_upgrade=True,
         apply=lambda h, s: _apply_stat(h, s, "max_hp", 10)),
    dict(name="Swift Feet", desc="+10% Move Speed", rarity="common", weight=3,
         global_upgrade=True,
         apply=lambda h, s: _apply_pct(h, s, "move_speed", 0.10)),
    dict(name="Sharp Edge", desc="+10% Damage", rarity="common", weight=3,
         global_upgrade=True,
         apply=lambda h, s: _apply_pct(h, s, "damage", 0.10)),
    dict(name="Magnet", desc="+10% Pickup Range", rarity="common", weight=3,
         global_upgrade=True,
         apply=lambda h, s: _apply_pct(h, s, "magnet_range", 0.10)),
    dict(name="Haste", desc="+10% Attack Speed", rarity="common", weight=3,
         global_upgrade=True,
         apply=lambda h, s: _apply_pct(h, s, "attack_speed", 0.10)),
    dict(name="Goliath", desc="+25 Max HP", rarity="uncommon", weight=2,
         global_upgrade=True,
         apply=lambda h, s: _apply_stat(h, s, "max_hp", 25)),
    dict(name="Wind Walker", desc="+20% Move Speed", rarity="uncommon", weight=2,
         global_upgrade=True,
         apply=lambda h, s: _apply_pct(h, s, "move_speed", 0.20)),
    dict(name="Sharpshooter", desc="+20% Damage", rarity="uncommon", weight=2,
         global_upgrade=True,
         apply=lambda h, s: _apply_pct(h, s, "damage", 0.20)),
    dict(name="Colossus Magnet", desc="+25% Pickup Range", rarity="uncommon", weight=2,
         global_upgrade=True,
         apply=lambda h, s: _apply_pct(h, s, "magnet_range", 0.25)),

    # ===== ROGUE SPECIFIC =====
    dict(name="Poison Master", desc="+1 Poison Stack on E", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "rogue",
         apply=lambda h, s: _apply_stat(h, s, "poison_stacks", 1)),
    dict(name="Venomous Blade", desc="+2 Poison DOT Damage", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "rogue",
         apply=lambda h, s: _apply_stat(h, s, "poison_dmg", 2)),
    dict(name="Shadow Step", desc="-1s Dash Cooldown", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "rogue",
         apply=lambda h, s: _apply_stat(h, s, "dash_cd_reduce", 1.0)),
    dict(name="Longshot", desc="+10% Attack Range", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "rogue",
         apply=lambda h, s: _apply_pct(h, s, "attack_range", 0.10)),
    dict(name="Throwing Knives", desc="Auto-fire 3 knives in a fan", rarity="rare", weight=1, min_level=5,
         hero_filter=lambda hk: hk == "rogue",
         apply=lambda h, s: _apply_weapon(h, s, "throwing_knives")),

    # ===== WARRIOR SPECIFIC =====
    dict(name="Endurance", desc="+1s Rally Heal Duration", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "warrior",
         apply=lambda h, s: _apply_stat(h, s, "rally_duration", 1.0)),
    dict(name="Iron Resolve", desc="+1s Iron Skin Duration", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "warrior",
         apply=lambda h, s: _apply_stat(h, s, "iron_skin_duration", 1.0)),
    dict(name="Earthquake", desc="+20% Slam Radius", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "warrior",
         apply=lambda h, s: _apply_pct(h, s, "slam_radius", 0.20)),
    dict(name="Fortress", desc="+50 Max HP, +1 Iron Skin", rarity="rare", weight=1,
         hero_filter=lambda hk: hk == "warrior",
         apply=lambda h, s: (_apply_stat(h, s, "max_hp", 50), _apply_stat(h, s, "iron_skin_duration", 1.0))),
    dict(name="Slam Fury", desc="-20% Slam Cooldown", rarity="rare", weight=1, min_level=5,
         hero_filter=lambda hk: hk == "warrior",
         apply=lambda h, s: _apply_pct(h, s, "slam_cooldown_reduce", 0.20)),

    # ===== WITCH SPECIFIC =====
    dict(name="Frost Mastery", desc="+1 Frost Bolt slow stack", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "witch",
         apply=lambda h, s: _apply_stat(h, s, "frost_slow_stacks", 1)),
    dict(name="Cryo Burst", desc="+2 Frost Bolt DOT (freeze tick)", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "witch",
         apply=lambda h, s: _apply_stat(h, s, "frost_dot_dmg", 2)),
    dict(name="Deep Freeze", desc="+1s Blizzard duration", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "witch",
         apply=lambda h, s: _apply_stat(h, s, "blizzard_duration", 1.0)),
    dict(name="Chain Freeze", desc="Ice Nova bounces to nearby enemies", rarity="rare", weight=1, min_level=5,
         hero_filter=lambda hk: hk == "witch",
         apply=lambda h, s: _apply_weapon(h, s, "chain_freeze")),
    dict(name="Absolute Zero", desc="Freeze +1s, enemies take 50% more dmg", rarity="rare", weight=1,
         hero_filter=lambda hk: hk == "witch",
         apply=lambda h, s: (_apply_stat(h, s, "freeze_duration", 1.0), _apply_stat(h, s, "frozen_bonus_dmg", 0.5))),

    # ===== ASSASSIN SPECIFIC =====
    dict(name="Night Stalker", desc="+5% Shadow Bolt homing speed", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "assassin",
         apply=lambda h, s: _apply_pct(h, s, "shadow_homing", 0.05)),
    dict(name="Assassinate", desc="+50% Shadow Step burst damage", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "assassin",
         apply=lambda h, s: _apply_pct(h, s, "shadow_step_dmg", 0.50)),
    dict(name="Double Shadow", desc="+1 clone, or clone damage +100%", rarity="uncommon", weight=2,
         hero_filter=lambda hk: hk == "assassin",
         apply=lambda h, s: _apply_stat(h, s, "shadow_clones", 1)),
    dict(name="Shadow Surge", desc="Shadow Step also teleports to frozen enemies", rarity="rare", weight=1,
         hero_filter=lambda hk: hk == "assassin",
         apply=lambda h, s: _apply_stat(h, s, "shadow_surge", 1)),
 dict(name="Eclipse", desc="Shadow Clone explodes into 5 homing shadow bolts", rarity="rare", weight=1,
         hero_filter=lambda hk: hk == "assassin",
         apply=lambda h, s: _apply_weapon(h, s, "eclipse")),

    # ===== PASSIVE ABILITIES — universal =====
    dict(name="Critical Strike", desc="15% chance for 2x damage", rarity="uncommon", weight=2,
         global_upgrade=True, passive="crit", value=0.15,
         apply=lambda h, s: _apply_pct(h, s, "crit_chance", 0.15)),
    dict(name="Lifesteal", desc="Heal 3 HP on hit", rarity="uncommon", weight=2,
         global_upgrade=True, passive="lifesteal", value=3,
         apply=lambda h, s: _apply_stat(h, s, "lifesteal", 3)),
    dict(name="Evasion", desc="10% chance to dodge attacks", rarity="uncommon", weight=2,
         global_upgrade=True, passive="evasion", value=0.10,
         apply=lambda h, s: _apply_pct(h, s, "evasion", 0.10)),
    dict(name="Thorns", desc="Reflect 4 damage back on hit", rarity="uncommon", weight=2,
         global_upgrade=True, passive="thorns", value=4,
         apply=lambda h, s: _apply_stat(h, s, "thorns", 4)),
    dict(name="Siphon", desc="+3% damage, +3 HP on kill", rarity="uncommon", weight=2,
         global_upgrade=True, passive="siphon", value=3,
         apply=lambda h, s: (_apply_pct(h, s, "siphon_dmg", 0.03), _apply_stat(h, s, "siphon_heal", 3))),

    dict(name="Frenzy", desc="+3% attack speed per kill (stacks)", rarity="rare", weight=1,
         global_upgrade=True, passive="frenzy", value=0.03,
         apply=lambda h, s: _apply_pct(h, s, "frenzy_per_kill", 0.03)),
    dict(name="Armor", desc="-3 damage taken", rarity="rare", weight=1,
         global_upgrade=True, passive="armor", value=3,
         apply=lambda h, s: _apply_stat(h, s, "armor", 3)),
    dict(name="Replenish", desc="-8% cooldown on kill", rarity="rare", weight=1,
         global_upgrade=True, passive="replenish", value=0.08,
         apply=lambda h, s: _apply_pct(h, s, "replenish", 0.08)),
    dict(name="Second Wind", desc="Heal 5 HP on kill", rarity="rare", weight=1,
         global_upgrade=True, passive="second_wind", value=5,
         apply=lambda h, s: _apply_stat(h, s, "second_wind", 5)),
    dict(name="Executioner", desc="Deal 3x damage to enemies below 30% HP", rarity="rare", weight=1,
         global_upgrade=True, passive="executioner", value=3.0, threshold=0.30,
         apply=lambda h, s: (_apply_stat(h, s, "executioner_mult", 3.0), _apply_stat(h, s, "executioner_threshold", 0.30))),
]