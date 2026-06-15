"""Procedural sound effects using pygame.sndarray."""
import pygame as pg
import numpy as np
from survivors import config as C


class SFXManager:
    def __init__(self):
        self._sounds = {}
        freq, bits, ch = pg.mixer.get_init() or (22050, -16, 2)
        self._channels = ch
        self._generate_all()

    def _make_sound(self, data):
        """Create sound from int16 numpy array, handling mono/stereo mismatch."""
        arr = data.astype(np.int16)
        if self._channels == 2 and arr.ndim == 1:
            arr = np.column_stack((arr, arr))
        return pg.sndarray.make_sound(arr)

    def _generate_all(self):
        sample_rate = 22050
        # Attack — short high blip
        self._sounds["attack"] = self._tone(0.08, 800, "sine", sample_rate, 0.15)
        # Hit — low thud
        self._sounds["hit"] = self._tone(0.1, 200, "triangle", sample_rate, 0.25)
        # Enemy death — descending sweep
        self._sounds["enemy_death"] = self._sweep(0.15, 600, 200, sample_rate, 0.2)
        # Level up — ascending arpeggio
        self._sounds["level_up"] = self._arpeggio(sample_rate, 0.3, 0.12)
        # Gem pickup — bright ping
        self._sounds["gem"] = self._tone(0.06, 1200, "sine", sample_rate, 0.1)
        # Dodge — whoosh
        self._sounds["dodge"] = self._sweep(0.12, 300, 1200, sample_rate, 0.15)
        # Slam — deep boom
        self._sounds["slam"] = self._tone(0.2, 80, "sine", sample_rate, 0.35)
        # Poison — hiss
        self._sounds["poison"] = self._noise(0.15, sample_rate, 0.12)
        # Shield — metallic chime
        self._sounds["shield"] = self._tone(0.25, 1500, "sine", sample_rate, 0.1, decay=0.6)
        # Heal — warm ascending
        self._sounds["heal"] = self._sweep(0.2, 400, 800, sample_rate, 0.12)
        # Boss warning
        self._sounds["boss"] = self._tone(0.3, 100, "sawtooth", sample_rate, 0.2)
        # Upgrade select — short bright ping
        self._sounds["select"] = self._tone(0.04, 1400, "sine", sample_rate, 0.08)

    def play(self, name):
        if name in self._sounds:
            try:
                self._sounds[name].play()
            except pg.error:
                pass

    def _tone(self, duration, freq, wave_type, sr, volume=0.2, decay=0.3):
        n = int(duration * sr)
        t = np.linspace(0, duration, n, dtype=np.float32)
        if wave_type == "sine":
            data = np.sin(2 * np.pi * freq * t)
        elif wave_type == "triangle":
            data = 2 * np.abs(2 * (freq * t % 1) - 1) - 1
        elif wave_type == "sawtooth":
            data = 2 * (freq * t % 1) - 1
        else:
            data = np.sin(2 * np.pi * freq * t)
        env = np.exp(-t * decay / duration * 4)
        data *= env
        data *= volume
        return self._make_sound(data * 32767)

    def _sweep(self, duration, f_start, f_end, sr, volume=0.2):
        n = int(duration * sr)
        t = np.linspace(0, duration, n, dtype=np.float32)
        freqs = np.linspace(f_start, f_end, n)
        data = np.zeros(n, dtype=np.float32)
        phase = 0.0
        for i in range(n):
            data[i] = np.sin(2 * np.pi * freqs[i] * (1.0 / sr))
            phase += freqs[i] / sr
        env = np.exp(-t * 3.0 / duration)
        data *= env * volume
        return self._make_sound(data * 32767)

    def _arpeggio(self, sr, duration, volume=0.1):
        notes = [523, 659, 784, 1047]  # C5, E5, G5, C6
        part_dur = duration / len(notes)
        parts = []
        for freq in notes:
            n = int(part_dur * sr)
            t = np.linspace(0, part_dur, n, dtype=np.float32)
            data = np.sin(2 * np.pi * freq * t) * np.exp(-t * 5.0 / part_dur) * volume
            parts.append((data * 32767).astype(np.int16))
        combined = np.concatenate(parts)
        return self._make_sound(combined)

    def _noise(self, duration, sr, volume=0.1):
        n = int(duration * sr)
        data = np.random.randn(n).astype(np.float32) * volume
        env = np.exp(-np.linspace(0, duration, n) * 8.0 / duration)
        data *= env
        return self._make_sound(data * 8000)


# Singleton
sfx = None


def init_sfx():
    global sfx
    sfx = SFXManager()


def play(name):
    if sfx:
        sfx.play(name)