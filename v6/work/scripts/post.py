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
    # ревизия: фон темнее на ~10% (правко пользователя)
    dark = np.array([4.5, 15.3, 9.9], np.float32)
    light = np.array([20.7, 50.4, 34.2], np.float32)
    rgb = dark[None, None, :] + (light - dark)[None, None, :] * lum[:, :, None]
    sp = rng.random((n, n))
    mask = (sp > 0.999).astype(np.float32)
    mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(0.8))) / 255.0
    rgb += mask[:, :, None] * np.array([16, 30, 20], np.float32)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def zhang_suen(m):
    """Тонкая скелетизация 8-связной маски (Zhang-Suen), периодические границы.
    Гарантирует непрерывность линий: тонкие/бледные сегменты не рвутся порогом."""
    m = m.astype(np.uint8).copy()
    while True:
        changed = False
        for step in (1, 2):
            P = m
            p2 = np.roll(P, -1, 0)
            p3 = np.roll(p2, -1, 1)
            p4 = np.roll(P, -1, 1)
            p5 = np.roll(p4, 1, 0)
            p6 = np.roll(p5, 1, 1)
            p7 = np.roll(P, 1, 1)
            p8 = np.roll(p7, 1, 0)
            p9 = np.roll(P, 1, 0)
            B = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
            A = (((p2 == 0) & (p3 == 1)).astype(int) + ((p3 == 0) & (p4 == 1)).astype(int)
                 + ((p4 == 0) & (p5 == 1)).astype(int) + ((p5 == 0) & (p6 == 1)).astype(int)
                 + ((p6 == 0) & (p7 == 1)).astype(int) + ((p7 == 0) & (p8 == 1)).astype(int)
                 + ((p8 == 0) & (p9 == 1)).astype(int) + ((p9 == 0) & (p2 == 1)).astype(int))
            c1 = (B >= 2) & (B <= 6) & (A == 1) & (P == 1)
            c2 = ((p2 * p4 * p6 == 0) & (p4 * p6 * p8 == 0)) if step == 1 \
                else ((p2 * p4 * p8 == 0) & (p2 * p6 * p8 == 0))
            rm = c1 & c2
            m[rm] = 0
            changed = changed or rm.any()
        if not changed:
            break
    return m


def crackle_tile():
    """Кракелюр формы crackle2 (принята пользователем), сетка в ~5 раз крупнее,
    линии тонкие и непрерывные: скелет гребня (1px) с модуляцией яркостью
    оригинала. Бесшовность: апскейл x5 сохраняет период, зеркальная сшивка окна."""
    c = np.asarray(sq(load('crackle2')).convert('L'))
    hp = np.clip(128 + (highpass(c, 24) - 128) * 3.6, 0, 255)
    t640 = mirror_tile(np.stack([hp] * 3, axis=2).astype(np.uint8), 640)
    u = t640.resize((3200, 3200), Image.LANCZOS).convert('L')
    win = u.crop((1280, 1280, 1920, 1920))
    tile = mirror_tile(np.stack([np.asarray(win)] * 3, axis=2), 640).convert('L')
    g = np.asarray(tile).astype(np.float32)
    d = np.clip(g - 128, 0, 255)               # трещины в источнике СВЕТЛЫЕ
    sk = zhang_suen(d > 25)
    p995 = np.percentile(d, 99.5)
    inten = np.clip(d / (p995 + 1e-6) * 2.2, 0.28, 1.0)
    lines = np.clip(sk.astype(np.float32) * inten, 0, 1)
    lines = np.asarray(Image.fromarray((lines * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) / 255.0
    out = np.clip(128 + lines * 110, 0, 255)
    return Image.fromarray(np.stack([out] * 3, axis=2).astype(np.uint8))


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
    """Портрет автора: тёплый дуотон в свете свечи, фигура выступает из темноты."""
    try:
        im = Image.open(f'/home/pi/workspace/labfem/v6/spec/{src}.png').convert('RGB')
    except OSError as exc:
        raise SystemExit(f'не удалось открыть портрет {src}: {exc}') from None
    im = crop_ratio(im, 2, 3)
    im = im.resize((700, 1050), Image.LANCZOS)
    im = duotone(im, shadow=(28, 18, 9), light=(241, 221, 178))
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    y, x = np.mgrid[0:h, 0:w]
    r = np.sqrt(((x - w / 2) / (w * 0.60)) ** 2 + ((y - h * 0.44) / (h * 0.60)) ** 2)
    m = np.clip(1.18 - r, 0, 1) ** 1.5          # 1 в центре, 0 к краям
    factor = (0.16 + 0.84 * m)[:, :, None]      # края тонут в темноте
    a = np.clip(a * factor, 0, 255)
    im = Image.fromarray(a.astype(np.uint8))
    save_webp(grain_vignette(im, vig=0.10), f'{SITE}/authors/{out}.webp')


def inset_crop(im, frac):
    """Обрезать светлую бумажную кайму по краям генерации."""
    try:
        w, h = im.size
        dx, dy = int(w * frac), int(h * frac)
        return safe_crop(im, (dx, dy, w - dx, h - dy))
    except Exception as exc:
        raise SystemExit(f'inset-кроп {frac} не удался: {exc}') from None


def main():
    # --- тайлы текстур ---
    save_webp(velvet_tile(), f'{SITE}/tex/velvet-tile.webp')
    save_webp(seamless_tile(load('gold-tile'), 256), f'{SITE}/tex/gold-tile.webp')
    save_webp(seamless_tile(load('parchment-tile'), 512), f'{SITE}/tex/parchment-tile.webp')

    # --- картины (v7: medieval/tapestry restyle, т2и-оригиналы из work/img-raw) ---
    # антракт: t2i, 1280x1600 → 1460x1825, лёгкий unsharp (t2i уже резкий, усиления не надо)
    hero2 = load('v7-interlude-1').resize((1460, 1825), Image.LANCZOS)
    hero2 = hero2.filter(ImageFilter.UnsharpMask(radius=2.0, percent=55, threshold=2))
    save_webp(grain_vignette(hero2), f'{SITE}/hero/hero-canvas-2.webp')
    # полноэкранное полотно: v7-hero-1, зеркалим (лицо в источнике слева, тексту нужен правый край),
    # два кропа одного оригинала: desktop 16:9 1600x900, mobile 9:16 1152x2048
    hf = load('v7-hero-1').transpose(Image.FLIP_LEFT_RIGHT)
    land = hf.crop((208, 0, 2048, 1035))  # голова ровно по центру (50%), макушка ~10%
    save_webp(grain_vignette(land), f'{SITE}/hero/hero-full-land.webp')
    port = hf.crop((552, 0, 1704, 2048))  # голова по центру (50%), целиком над текстом
    save_webp(grain_vignette(port), f'{SITE}/hero/hero-full-port.webp')
    # --- feminity-figure-2: внешний референс (v8-neck), кроп 4:5 + изумрудный сплит-тон ---
    neck = load('v8-neck').convert('RGB').crop((8, 57, 862, 1125))
    na = np.asarray(neck).astype(np.float32)
    lum = na.mean(axis=2, keepdims=True) / 255.0
    shadow = np.clip((0.45 - lum) / 0.45, 0, 1)  # мягкая маска теней
    na[..., 0] -= 10 * shadow[..., 0]
    na[..., 1] += 14 * shadow[..., 0]
    na[..., 2] += 8 * shadow[..., 0]
    na = np.clip(na * 1.03, 0, 255)  # лёгкий контраст
    neck = Image.fromarray(na.astype(np.uint8)).resize((800, 1000), Image.LANCZOS)
    save_webp(grain_vignette(neck), f'{SITE}/paint/feminity-figure-2.webp')

    # --- optics-figure: внешний референс (v8-face, девушка с птицей), кроп 4:5 + изумруд ---
    face = load('v8-face').convert('RGB').crop((170, 50, 1005, 1094))
    fa = np.asarray(face).astype(np.float32)
    lum = fa.mean(axis=2, keepdims=True) / 255.0
    shadow = np.clip((0.45 - lum) / 0.45, 0, 1)
    fa[..., 0] -= 10 * shadow[..., 0]
    fa[..., 1] += 14 * shadow[..., 0]
    fa[..., 2] += 8 * shadow[..., 0]
    fa = np.clip(fa * 1.03, 0, 255)
    face = Image.fromarray(fa.astype(np.uint8)).resize((800, 1000), Image.LANCZOS)
    save_webp(grain_vignette(face), f'{SITE}/paint/optics-figure.webp')

    # --- for-whom-figure: внешний референс (v8-pearls, жемчужный каскад) ---
    pearls = load('v8-pearls').convert('RGB')
    pa = np.asarray(pearls).astype(np.float32)
    rng = np.random.default_rng(7)
    def patch(x0, y0, x1, y1, lx0, lx1, rx0, rx1):
        left = pa[y0:y1, lx0:lx1].mean(axis=1)      # (h,3) на строку
        right = pa[y0:y1, rx0:rx1].mean(axis=1)
        w = x1 - x0
        t = (np.arange(w) / (w - 1))[None, :, None]
        grad = left[:, None, :] * (1 - t) + right[:, None, :] * t
        grad += rng.normal(0, 2.0, grad.shape)
        pa[y0:y1, x0:x1] = np.clip(grad, 0, 255)
    patch(18, 108, 135, 268, 5, 16, 140, 151)       # крестик
    patch(788, 108, 918, 262, 774, 786, 920, 929)   # точки
    patch(0, 0, 56, 136, 60, 76, 60, 76)            # дуга скругления слева
    patch(872, 0, 930, 136, 854, 868, 854, 868)     # дуга скругления справа
    pearls = Image.fromarray(pa.astype(np.uint8)).crop((8, 103, 922, 1245))
    qa = np.asarray(pearls).astype(np.float32)
    lum = qa.mean(axis=2, keepdims=True) / 255.0
    shadow = np.clip((0.45 - lum) / 0.45, 0, 1)
    qa[..., 0] -= 10 * shadow[..., 0]
    qa[..., 1] += 14 * shadow[..., 0]
    qa[..., 2] += 8 * shadow[..., 0]
    qa = np.clip(qa * 1.03, 0, 255)
    pearls = Image.fromarray(qa.astype(np.uint8)).resize((800, 1000), Image.LANCZOS)
    save_webp(grain_vignette(pearls), f'{SITE}/paint/for-whom-figure.webp')

    pairs = [
             ('v7-circle-1', 'paint/circle-figure-3'),
             ('v7-invite-1', 'paint/invite-figure'),
             ('v7-cat-2', 'cards/cat-black'),
             ('v7-pomegranate-1', 'cards/pomegranate'),
             ('v7-snake-2', 'cards/snake-skin'),
             ('v7b-spindle-2', 'cards/thread-spindle'),
             ('v7-water-2', 'cards/water-dark')]
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

    # --- og-cover: кроп v7-interlude-1 1200x630 ---
    og = crop_cover(load('v7-interlude-1'))
    save_webp(grain_vignette(og.resize((1200, 630), Image.LANCZOS)), f'{SITE}/meta/og-cover.webp')
    print('done')


if __name__ == '__main__':
    main()
