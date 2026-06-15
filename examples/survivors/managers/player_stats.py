"""Player progression: XP, level, ability levels, cooldowns."""


class PlayerStats:
    def __init__(self, max_hp, abilities):
        self.max_hp = max_hp
        self.hp = max_hp
        self.xp = 0
        self.level = 1
        self.xp_to_next = 20
        self.abilities = dict(abilities)  # {"slash": 1, "dash": 0, "poison": 0}
        self.cooldowns = {k: 0.0 for k in abilities}
        self.kills = 0
        self.active_effects = {}  # ability_name -> remaining_seconds (for buffs like iron_skin)

    def add_xp(self, amount):
        self.xp += amount
        leveled = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.5)
            leveled = True
        return leveled

    @property
    def xp_fraction(self):
        return self.xp / self.xp_to_next

    @property
    def hp_fraction(self):
        return self.hp / self.max_hp

    def take_damage(self, dmg):
        reduction = 0.0
        if "iron_skin" in self.active_effects and self.active_effects["iron_skin"] > 0:
            reduction = 0.5
        actual = int(dmg * (1.0 - reduction))
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_on_cooldown(self, ability):
        return self.cooldowns.get(ability, 0.0) > 0

    def update_cooldowns(self, dt):
        for k in self.cooldowns:
            if self.cooldowns[k] > 0:
                self.cooldowns[k] -= dt
        for k in self.active_effects:
            if self.active_effects[k] > 0:
                self.active_effects[k] -= dt

    def start_effect(self, ability, duration):
        self.active_effects[ability] = duration