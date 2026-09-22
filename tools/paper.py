#!/usr/bin/env python3
"""Сырая бумага от модели -> прозрачные фактуры старения (webp).

В отличие от гравюр (ink.py), лист здесь ровный целиком, поэтому фон оцениваем
глобально (95-й перцентиль по каналам — это чистая бумага), а альфа = насколько
пиксель темнее листа: так выживают и крупные разводы, и мелкое зерно. Силу
держим двумя числами (gain, cap) — «в меру» должно настраиваться, а не
угадываться. Зерно (t1) сшиваем в бесшовную плитку зеркалом по четвертям.
Запуск: .venv/bin/python tools/paper.py [id ...] [--out=DIR]
"""
import sys
from pathlib import Path

import numpy as np  # pyright: ignore[reportMissingImports] — пакет лежит в проектном .venv
from PIL import Image, ImageFilter  # pyright: ignore[reportMissingImports] — пакет лежит в проектном .venv

from manifest import ASSETS, PAPER

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets-src"
OUT = ROOT / "site_v2" / "assets" / "img"

# id: (gain, cap, blur, width) — долю темноты листа, идущую в альфу, её потолок,
# сглаживание альфы (jpeg-шум сырья иначе лезет в альфу «грязью» и раздувает webp)
# и ширину готового файла: байты здесь дороже пикселей, фактуры мягкие
TUNE = {
    "t1-paper": (.45, .07, .8, 512),
    "t2-bloom": (.85, .07, 2.2, 560),
}


def cut_flat(im: Image.Image, gain: float, cap: float) -> np.ndarray:
    """RGB на ровном листе -> RGBA (0..255), цвет следов сохраняем как есть."""
    c = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    bg = np.maximum(np.percentile(c, 95, axis=(0, 1)), 1e-3)
    alpha = np.clip((1.0 - c / bg).max(axis=2), 0.0, 1.0)
    alpha = np.clip(alpha * gain, 0.0, cap)
    a3 = np.maximum(alpha[..., None], 1e-3)
    fg = np.clip((c - (1.0 - alpha[..., None]) * bg) / a3, 0.0, 1.0)
    return (np.dstack([fg, alpha]) * 255.0).astype(np.uint8)


def seamless(rgba: np.ndarray) -> np.ndarray:
    """Зеркало по четвертям: швов нет по построению."""
    h, w = rgba.shape[0] // 2, rgba.shape[1] // 2
    q = rgba[:h, :w]
    top = np.concatenate([q, q[:, ::-1]], axis=1)
    return np.concatenate([top, top[::-1]], axis=0)


def process(aid: str) -> str:
    """Один ассет; битый сырой файл не роняет весь батч (как в ink.py)."""
    try:
        src = max((p for p in (RAW / f"{aid}.png", RAW / f"{aid}.jpg") if p.exists()),
                  key=lambda p: p.stat().st_mtime, default=None)
        if src is None:
            return f"skip {aid} (нет сырья)"
        gain, cap, blur, width = TUNE[aid]
        rgba = cut_flat(Image.open(src), gain, cap)
        if blur:
            im = Image.fromarray(rgba, "RGBA")
            im.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(blur)))
            rgba = np.asarray(im)
        if aid == "t1-paper":
            rgba = seamless(rgba)
        im = Image.fromarray(rgba, "RGBA")
        if im.width != width:  # разводы и зерно мягкие, даунскейл им не страшен, а байты — да
            k = width / im.width
            im = im.resize((width, round(im.height * k)), Image.Resampling.LANCZOS)
            rgba = np.asarray(im)
        OUT.mkdir(parents=True, exist_ok=True)
        dst = OUT / f"{aid}.webp"
        opt = ASSETS[aid][4] if len(ASSETS[aid]) > 4 else {}
        Image.fromarray(rgba, "RGBA").save(dst, "WEBP", quality=int(opt.get("lossy", 82)), method=6)
        return (f"ok   {aid} {rgba.shape[1]}x{rgba.shape[0]} "
                f"альфа сред {rgba[..., 3].mean() / 2.55:.1f}% -> {dst.stat().st_size // 1024}KB")
    except Exception as err:  # noqa: BLE001 — намеренно широко: это пакетный скрипт
        return f"FAIL {aid}: {err}"


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg.startswith("--out="):
            OUT = (ROOT / arg[6:]).resolve() if not arg[6:].startswith("/") else Path(arg[6:])
    ids = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PAPER)
    for aid in ids:
        print(process(aid), flush=True)
