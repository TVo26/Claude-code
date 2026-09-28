# Code-made sound track: marker squeaks, page whooshes, dings/womps, light music bed.
import json, wave, numpy as np, sys
d = json.load(open(sys.argv[1])); SR = 44100; DUR = d['DUR']; N = int(SR * DUR)
rng = np.random.default_rng(7); out = np.zeros(N)
def band(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)
def put(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if j > i: out[i:j] += sig[:j - i] * g
env = lambda n, a, r: np.minimum(1, np.minimum(np.arange(n) / max(1, a * SR), (n - np.arange(n)) / max(1, r * SR)))
# marker: scratchy noise with stroke-rate wobble
for it in d['TL']:
    n = int((it['t1'] - it['t0']) * SR);
    if n < 200: continue
    tt = np.arange(n) / SR; rate = 9 if it['text'] else 5
    am = .55 + .45 * np.abs(np.sin(np.pi * rate * tt + it['t0'] * 3))
    put(band(n, 2500, 7000) * am * env(n, .01, .03), it['t0'], .10)
    put(band(n, 900, 1800) * am * env(n, .01, .03), it['t0'], .05)
# whoosh on each board slide
for c in d['CUTS']:
    n = int(.55 * SR); tt = np.arange(n) / n
    put(band(n, 300, 3000) * np.sin(np.pi * tt) ** 2, c - .02, .22)
def tone(freqs, dur, dec, g=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; y = sum(np.sin(2 * np.pi * f * tt) * a for f, a in freqs)
    return y * np.exp(-tt / dec) * env(n, .004, .05) * g
for it in d['TL']:
    if it['ding']: put(tone([(1318.5, 1), (1975.5, .5), (2637, .25)], .8, .25), it['t1'] - .05, .16)
    if it['womp']:
        n = int(.5 * SR); tt = np.arange(n) / SR; f = 220 * np.exp(-tt * 1.4)
        put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .25) * env(n, .005, .05), it['t1'] - .05, .20)
# music bed: plucked arpeggio C–G–Am–F at 104 bpm + soft bass + shaker
beat = 60 / 104; chords = [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def pluck(f, dur=.45):
    n = int(dur * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + .35 * np.sin(4 * np.pi * f * tt) + .12 * np.sin(6 * np.pi * f * tt)) * np.exp(-tt / .14) * env(n, .003, .05)
t = 0.0; k = 0; pat = [0, 2, 1, 3, 2, 1, 3, 2]
while t < DUR:
    ch = chords[(k // 8) % 4]
    put(pluck(hz(ch[pat[k % 8]] + 12)), t, .07)
    if k % 8 == 0: put(tone([(hz(ch[0] - 12), 1), (hz(ch[0]), .3)], beat * 3.8, 1.0), t, .09)
    if k % 2 == 1: n = int(.06 * SR); put(band(n, 6000, 12000) * np.exp(-np.arange(n) / SR / .015), t, .05)
    t += beat / 2; k += 1
fade = np.ones(N); m = int(.6 * SR); fade[-m:] = np.linspace(1, 0, m); fade[:int(.02 * SR)] = np.linspace(0, 1, int(.02 * SR))
out *= fade; out = np.tanh(out * 1.4) / np.tanh(1.4); out *= .89 / np.abs(out).max()
with wave.open(sys.argv[2], 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes())
print('ok', N / SR)
