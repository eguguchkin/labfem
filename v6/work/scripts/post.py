#!/usr/bin/env python3
"""Постобработка ассетов labfem v6: тайлы (зеркальная сшивка), webp, альфа, дуотон.

Запуск: /tmp/imgenv/bin/python post.py  (venv с PIL/numpy; системный python их не имеет,
поэтому импорты ниже помечены type: ignore — линтер вне venv их не видит).
Одноразовый производственный скрипт этапа 1; вход — work/img-raw/*.png.
"""
import os

import numpy as np  # type: ignore[import-not-found]
from PIL import Image, ImageFilter  # type: ignore[import-not-found]

RAW = '/home/pi/workspace/labfem/v6/work/img-raw'
SITE = '/home/pi/workspace/labfem/v6/site/assets/img'


def makedirs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as exc:
        raise SystemExit(f'не удалось создать каталог {path}: {exc}') from None


for d in ['tex', 'hero', 'paint', 'cards', 'orn', 'authors', 'meta']:
    makedirs(f'{SITE}/{d}')


def load(name):
    try:
        return Image.open(f'{RAW}/{name}.png').convert('RGB')
    except OSError as exc:
        raise SystemExit(f'не удалось открыть {RAW}/{name}.png: {exc}') from None


def save_webp(im, path, q=82):
    try:
        im.save(path, 'WEBP', quality=q, method=6)
    except OSError as exc:
        raise SystemExit(f'не удалось записать {path}: {exc}') from None
    print(path, im.size, os.path.getsize(path) // 1024, 'KB')


def safe_crop(im, box):
    try:
        return im.crop(box)
    except Exception as exc:
        raise SystemExit(f'кроп {box} не удался: {exc}') from None


def mirror_tile(a, out_size):
    """Зеркальная сшивка 2x2 массива HxWx3 -> бесшовный тайл out_size."""
    top = np.concatenate([a, a[:, ::-1]], axis=1)
    bot = np.concatenate([a[::-1], a[::-1][:, ::-1]], axis=1)
    tile = Image.fromarray(np.clip(np.concatenate([top, bot], axis=0), 0, 255).astype(np.uint8))
    return tile.resize((out_size, out_size), Image.LANCZOS)


def seamless_tile(im, out_size):
    """Центральная квадратная кропка -> зеркальная сшивка 2x2 -> даунскейл."""
    w, h = im.size
    s = min(w, h)
    im = safe_crop(im, ((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
    im = im.resize((512, 512))
    return mirror_tile(np.asarray(im), out_size)


def sq(im):
    """Центральная квадратная кропка 512x512."""
    w, h = im.size
    s = min(w, h)
    return safe_crop(im, ((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2)).resize((512, 512))


def highpass(gray, sigma):
    """Убрать низкочастотное освещение: оставить только фактуру (для сшивки)."""
    low = np.asarray(Image.fromarray(gray.astype(np.uint8))
                     .filter(ImageFilter.GaussianBlur(sigma))).astype(np.float32)
    return gray.astype(np.float32) / (low + 1e-3) * 128.0


def periodic_field(rng, n, lo, hi, aniso=1.0, power=2.0):
    """Периодическое fbm-поле через FFT: бесшовно по построению."""
    fy = np.fft.fftfreq(n)[:, None]
    fx = np.fft.rfftfreq(n)[None, :]
    lo, hi = lo / n, hi / n
    f = np.sqrt((fx * aniso) ** 2 + fy ** 2)
    f[0, 0] = 1.0
    amp = 1.0 / (f ** power)
    amp[(f < lo) | (f > hi)] = 0
    ph = rng.uniform(0, 2 * np.pi, (n, n // 2 + 1))
    spec = amp * np.exp(1j * ph)
    spec[0, 0] = 0
    fld = np.fft.irfft2(spec, s=(n, n))
    return (fld - fld.mean()) / (fld.std() + 1e-9)


def velvet_tile(n=1024):
    """Процедурный бархат: fbm-пятна + анизотропный ворс + редкие блики ворсинок."""
    rng = np.random.default_rng(77)
    base = periodic_field(rng, n, 1, 6, power=2.0)
    mid = periodic_field(rng, n, 6, 30, power=1.7)
    nap = periodic_field(rng, n, 80, 400, aniso=0.5, power=1.1)
    lum = base * 0.22 + mid * 0.30 + nap * 0.55
    lum = (lum - lum.min()) / (lum.max() - lum.min() + 1e-9)
    lum = lum ** 1.3
    dark = np.array([5, 17, 11], np.float32)
    light = np.array([23, 56, 38], np.float32)
    rgb = dark[None, None, :] + (light - dark)[None, None, :] * lum[:, :, None]
    sp = rng.random((n, n))
    mask = (sp > 0.999).astype(np.float32)
    mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(0.8))) / 255.0
    rgb += mask[:, :, None] * np.array([16, 30, 20], np.float32)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def crackle_tile():
    """Кракелюр из crackle2: highpass трещин + зеркальная сшивка 640."""
    c = np.asarray(sq(load('crackle2')).convert('L'))
    hp = np.clip(128 + (highpass(c, 24) - 128) * 1.9, 0, 255)
    return mirror_tile(np.stack([hp] * 3, axis=2).astype(np.uint8), 640)


def grain_vignette(im, sigma=1.2, amp=3.0, vig=0.06):
    a = np.asarray(im).astype(np.int16)
    rng = np.random.default_rng(7)
    noise = rng.normal(0, sigma, a.shape[:2])[:, :, None] * amp
    a = np.clip(a + noise, 0, 255)
    h, w = a.shape[:2]
    y, x = np.mgrid[0:h, 0:w]
    cy, cx = (h - 1) / 2, (w - 1) / 2
    r = np.sqrt(((x - cx) / cx) ** 2 + ((y - cy) / cy) ** 2)
    m = np.clip((r - 0.75) / 0.45, 0, 1) ** 2 * vig
    a = a * (1 - m[:, :, None])
    return Image.fromarray(a.astype(np.uint8))


def alpha_from_black(im, thr=26, soft=60):
    """Альфа по яркости: чёрный фон -> прозрачность (для золота на чёрном)."""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    lum = a.max(axis=2)
    alpha = np.clip((lum - thr) / (soft - thr + 1e-6), 0, 1)
    alpha = (alpha * 255).astype(np.uint8)
    out = im.convert('RGB').copy()
    out.putalpha(Image.fromarray(alpha))
    return out


def duotone(im, shadow=(10, 36, 23), light=(232, 219, 192)):
    g = np.asarray(im.convert('L')).astype(np.float32) / 255.0
    g = np.clip((g - 0.06) / 0.88, 0, 1) ** 0.95
    sh = np.array(shadow, np.float32)
    lt = np.array(light, np.float32)
    rgb = sh[None, None, :] * (1 - g[:, :, None]) + lt[None, None, :] * g[:, :, None]
    return Image.fromarray(rgb.astype(np.uint8))


def crop_ratio(im, rw, rh):
    """Кроп по пропорции rw:rh: по горизонтали центр, по вертикали верх."""
    try:
        w, h = im.size
        tw = w
        th = int(w * rh / rw)
        if th > h:
            th = h
            tw = int(h * rw / rh)
        return safe_crop(im, ((w - tw) // 2, 0, (w + tw) // 2, th))
    except Exception as exc:
        raise SystemExit(f'кроп по пропорции {rw}:{rh} не удался: {exc}') from None


def crop_cover(im):
    """Кроп под og-cover 1200x630 по центру."""
    try:
        w, h = im.size
        if w > h * 1200 / 630:
            box = ((w - int(h * 1200 / 630)) // 2, 0, (w + int(h * 1200 / 630)) // 2, h)
        else:
            box = (0, (h - int(w * 630 / 1200)) // 2, w, (h + int(w * 630 / 1200)) // 2)
        return safe_crop(im, box)
    except Exception as exc:
        raise SystemExit(f'кроп og-cover не удался: {exc}') from None


def portrait(src, out):
    try:
        im = Image.open(f'/home/pi/workspace/labfem/v6/spec/{src}.png').convert('RGB')
    except OSError as exc:
        raise SystemExit(f'не удалось открыть портрет {src}: {exc}') from None
    im = crop_ratio(im, 2, 3)
    im = im.resize((700, 1050), Image.LANCZOS)
    im = duotone(im)
    save_webp(grain_vignette(im, vig=0.10), f'{SITE}/authors/{out}.webp')


def main():
    # --- тайлы текстур ---
    save_webp(velvet_tile(), f'{SITE}/tex/velvet-tile.webp')
    save_webp(crackle_tile(), f'{SITE}/tex/crackle-tile.webp')
    save_webp(seamless_tile(load('gold-tile'), 256), f'{SITE}/tex/gold-tile.webp')
    save_webp(seamless_tile(load('parchment-tile'), 512), f'{SITE}/tex/parchment-tile.webp')

    # --- картины ---
    hero = load('hero-canvas').resize((1100, 1375), Image.LANCZOS)
    save_webp(grain_vignette(hero), f'{SITE}/hero/hero-canvas.webp')
    pairs = [('fruit-ripe', 'paint/fruit-ripe'), ('cat-black', 'cards/cat-black'),
             ('pomegranate', 'cards/pomegranate'), ('snake-skin', 'cards/snake-skin'),
             ('thread-spindle', 'cards/thread-spindle'), ('warm-stone', 'cards/warm-stone')]
    for name, out in pairs:
        im = load(name).resize((800, 1000), Image.LANCZOS)
        save_webp(grain_vignette(im), f'{SITE}/{out}.webp')

    # --- орнамент и символы (альфа) ---
    fl = alpha_from_black(load('fleuron')).resize((160, 160), Image.LANCZOS)
    save_webp(fl, f'{SITE}/orn/fleuron.webp', q=90)
    for name in ['sym-mirror', 'sym-snake', 'sym-brush', 'sym-thread']:
        im = alpha_from_black(load(name)).resize((220, 220), Image.LANCZOS)
        save_webp(im, f'{SITE}/orn/{name}.webp', q=90)

    # --- портреты авторов: дуотон-сепия, кроп 2:3 ---
    portrait('author-polina', 'polina')
    portrait('author-veronika', 'veronika')

    # --- og-cover: кроп hero 1200x630 ---
    og = crop_cover(load('hero-canvas'))
    save_webp(grain_vignette(og.resize((1200, 630), Image.LANCZOS)), f'{SITE}/meta/og-cover.webp')
    print('done')


if __name__ == '__main__':
    main()
