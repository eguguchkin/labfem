#!/usr/bin/env python3
"""Превращает сырой PNG на плоском фоне в «чернила на прозрачном».

Модель отдаёт растр без альфы, поэтому фон восстанавливаем математически:
картинка — это C = a*F + (1-a)*B (чернила F с прозрачностью a поверх бумаги B).
Оцениваем B локально (max-фильтр — самое светлое в окрестности, т.е. бумага),
решаем обратно относительно a и F. Дальше trim по альфе, ресайз под целевую
ширину и webp. Запуск: .venv/bin/python tools/ink.py [id ...]
"""
import sys
from pathlib import Path

import numpy as np  # pyright: ignore[reportMissingImports] — пакет лежит в проектном .venv
from manifest import ASSETS, PAPER
from PIL import (  # pyright: ignore[reportMissingImports] — пакет лежит в проектном .venv
    Image,
    ImageFilter,
)

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets-src"
OUT = ROOT / "site" / "assets" / "img"  # перезаписывается через --out=DIR (site_v2 и др.)


def raw_for(aid: str):
    """CLI пишет .png или .jpg (по mime ответа), engrave.py — .png: берём свежайший."""
    cands = [p for p in (RAW / f"{aid}.png", RAW / f"{aid}.jpg", RAW / f"{aid}.jpeg") if p.exists()]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def cut(im: Image.Image) -> np.ndarray:
    """RGB на плоском фоне -> RGBA (0..255)."""
    rgb = im.convert("RGB")
    c = np.asarray(rgb, dtype=np.float32) / 255.0
    # самое светлое в окрестности — это бумага; считаем на 1/4 масштаба (быстрее),
    # blur сглаживает лёгкий градиент бумаги
    small = rgb.resize((rgb.width // 4, rgb.height // 4), Image.Resampling.BILINEAR)
    bg_small = small.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(8))
    bg_img = bg_small.resize(rgb.size, Image.Resampling.BILINEAR)
    bg = np.maximum(np.asarray(bg_img, dtype=np.float32) / 255.0, 1e-3)

    # alpha = насколько пиксель темнее/насыщеннее бумаги (максимум по каналам)
    alpha = np.clip(1.0 - c / bg, 0.0, 1.0).max(axis=2)
    alpha[alpha < 0.02] = 0.0
    alpha = np.clip(alpha * 1.08, 0.0, 1.0)  # тонкие линии чуть плотнее

    a3 = np.maximum(alpha[..., None], 1e-3)
    fg = np.clip((c - (1.0 - alpha[..., None]) * bg) / a3, 0.0, 1.0)
    return (np.dstack([fg, alpha]) * 255.0).astype(np.uint8)


def process(aid: str) -> str:
    """Один ассет; битый сырой файл не роняет весь батч."""
    try:
        src = raw_for(aid)
        if src is None:
            return f"skip {aid} (нет сырья)"
        dst = OUT / f"{aid}.webp"
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            return f"skip {aid} (готово)"
        width = ASSETS[aid][1]
        rgba = Image.fromarray(cut(Image.open(src)), "RGBA")

        alpha = np.asarray(rgba)[:, :, 3]
        ys, xs = np.nonzero(alpha > 8)
        if len(xs) == 0:
            return f"FAIL {aid}: пустая альфа"
        pad = 6
        box = (max(int(xs.min()) - pad, 0), max(int(ys.min()) - pad, 0),
               min(int(xs.max()) + pad, rgba.width), min(int(ys.max()) + pad, rgba.height))
        rgba = rgba.crop(box)

        k = width / rgba.width
        if k < 1:
            rgba = rgba.resize((width, max(1, round(rgba.height * k))), Image.Resampling.LANCZOS)

        OUT.mkdir(parents=True, exist_ok=True)
        dst = OUT / f"{aid}.webp"
        opt = ASSETS[aid][4] if len(ASSETS[aid]) > 4 else {}
        if opt.get("lossy"):
            # фотопортреты: lossless раздувает карандашную микротень в мегабайты
            rgba.save(dst, "WEBP", quality=int(opt["lossy"]), method=6)
        else:
            rgba.save(dst, "WEBP", lossless=True, method=6)
        return f"ok   {aid} {rgba.width}x{rgba.height} -> {dst.stat().st_size // 1024}KB"
    except Exception as err:  # noqa: BLE001 — намеренно широко: это пакетный скрипт
        return f"FAIL {aid}: {err}"


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg.startswith("--out="):  # своя папка назначения, например site_v2/assets/img
            OUT = (ROOT / arg[6:]).resolve() if not arg[6:].startswith("/") else Path(arg[6:])
    ids = [a for a in sys.argv[1:] if not a.startswith("--")] or [a for a in ASSETS if a not in PAPER]
    for aid in ids:
        print(process(aid), flush=True)
