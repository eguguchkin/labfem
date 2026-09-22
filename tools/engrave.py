#!/usr/bin/env python3
"""Гравюизация фотографий авторов: офорт из самого фото (сходство 100%).

Штриховка под 45/-45/90 градусов с толщиной линии по яркости, контур по
градиенту, пунктир в полутонах, живой дрожь-линии через сглаженный шум,
виньеточное затухание к краям листа. Результат — RGB на плоской бумаге
#F5F0E8 в assets-src/, дальше его режет ink.py как обычную гравюру.

Запуск: .venv/bin/python tools/engrave.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets-src"

# id: (файл-источник, кроп «голова и плечи», тон акварельной подкраски)
JOBS = {
    "p1-veronika": ("raw/автор-1-Вероника.Гугучкина.jpg", (300, 70, 780, 700), (201, 169, 160)),
    "p2-polina": ("raw/автор-2-Полина.Корнер.jpg", (170, 40, 740, 950), (184, 169, 201)),
}


def engrave(src: Path, box: tuple, wash: tuple) -> Image.Image:
    im = Image.open(src).convert("L").crop(box)
    im = im.filter(ImageFilter.MedianFilter(3))  # убирает блёстки/шум, бережёт края
    w, h = im.size
    lum = np.asarray(im, np.float32) / 255.0
    lum = np.clip((lum - 0.5) * 1.15 + 0.52, 0.0, 1.0)  # мягкий тон-кор
    dark = (1.0 - lum) ** 0.9

    rng = np.random.default_rng(7)
    jitter = (rng.random((h // 8 + 1, w // 8 + 1)) - 0.5)
    jitter = np.asarray(Image.fromarray(((jitter + 0.5) * 255).astype(np.uint8))
                        .resize((w, h), Image.Resampling.BILINEAR), np.float32) - 0.5

    xx, yy = np.meshgrid(np.arange(w), np.arange(h))

    def hatch(angle: float, period: float, thr: float) -> np.ndarray:
        rad = np.deg2rad(angle)
        u = xx * np.cos(rad) + yy * np.sin(rad) + jitter * 2.2
        width = np.clip((dark - thr) * 1.6, 0.0, 0.7)
        return ((u / period) % 1.0 < width).astype(np.float32)

    lines = np.maximum(np.maximum(hatch(45, 3.6, 0.05),
                                  hatch(-45, 3.6, 0.35)),
                       hatch(90, 4.4, 0.6))

    gx, gy = np.gradient(lum, axis=1), np.gradient(lum, axis=0)
    grad = np.hypot(gx, gy)
    grad_img = Image.fromarray((np.clip(grad * 6, 0, 1) * 255).astype(np.uint8))
    grad = np.asarray(grad_img.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255.0
    contour = np.clip(grad * 1.2 - 0.3, 0.0, 1.0)

    mid = ((dark > 0.3) & (dark < 0.7)).astype(np.float32)
    stipple = (rng.random((h, w)) < np.clip(dark - 0.3, 0, 0.4) * 0.4).astype(np.float32) * mid
    alpha = np.clip(lines * 0.9 + contour * 0.6 + stipple * 0.15, 0.0, 1.0)

    # виньетка: овал вокруг головы, края листа остаются чистой бумагой
    r = np.sqrt(((xx - w / 2) / (w * 0.46)) ** 2 + ((yy - h * 0.38) / (h * 0.5)) ** 2)
    alpha *= np.clip((1.15 - r) / 0.35, 0.0, 1.0) ** 1.5

    ink = np.array([0x3A, 0x32, 0x30], np.float32) / 255.0
    sepia = np.array([0x6B, 0x5B, 0x4E], np.float32) / 255.0
    color = ink * (0.55 + 0.45 * lum[..., None]) + sepia * (0.45 - 0.45 * lum[..., None])

    wash_a = np.clip(np.asarray(Image.fromarray((dark * 255).astype(np.uint8))
                                .filter(ImageFilter.GaussianBlur(18)), np.float32)
                     / 255.0 * 0.5, 0.0, 0.14)
    paper = np.array([0xF5, 0xF0, 0xE8], np.float32) / 255.0
    img = paper * (1 - wash_a[..., None]) + np.array(wash, np.float32) / 255.0 * wash_a[..., None]
    img = img * (1 - alpha[..., None]) + color * alpha[..., None]
    return Image.fromarray((img * 255).astype(np.uint8))


if __name__ == "__main__":
    RAW.mkdir(parents=True, exist_ok=True)
    for aid, (rel, box, wash) in JOBS.items():
        out = engrave(ROOT / rel, box, wash)
        out.save(RAW / f"{aid}.png")
        print(f"ok   {aid} {out.width}x{out.height}")
