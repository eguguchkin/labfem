#!/usr/bin/env python3
"""Генерация ассетов через CLI pi-image-gen, несколько процессов параллельно.

Сырые PNG кладёт в assets-src/. Уже существующие файлы пропускает (--force
перегенерирует всё). Использование:  python3 tools/gen.py [id ...] [--jobs N] [--force]
"""
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from manifest import ASSETS, TAIL

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets-src"
CLI = Path.home() / ".pi/agent/npm/node_modules/@bytetrue/pi-image-gen/skills/pi-image-gen/scripts/image-gen.mjs"


def gen(aid: str) -> str:
    size, _, prompt = ASSETS[aid]
    out = RAW / f"{aid}.png"
    req = json.dumps({
        "prompt": prompt + TAIL,
        "size": size,
        "filename": aid,
        "outputDir": str(RAW),
    })
    t0 = time.time()
    try:
        r = subprocess.run(["node", str(CLI), "generate"], input=req,
                           capture_output=True, text=True, timeout=600)
    except Exception as err:  # noqa: BLE001 — таймаут/падение CLI не роняет батч
        return f"FAIL {aid} ({time.time() - t0:.0f}s): {err}"
    dt = time.time() - t0
    if r.returncode != 0 or not out.exists():
        return f"FAIL {aid} ({dt:.0f}s): {(r.stderr or r.stdout).strip()[-300:]}"
    return f"ok   {aid} ({dt:.0f}s) {out.stat().st_size // 1024}KB"


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    jobs_raw = next((a.split("=")[1] for a in sys.argv if a.startswith("--jobs")), "4")
    try:
        jobs = int(jobs_raw)
    except ValueError:
        sys.exit(f"--jobs expects a number, got {jobs_raw!r}")
    force = "--force" in sys.argv
    RAW.mkdir(parents=True, exist_ok=True)

    todo = [a for a in (args or list(ASSETS))
            if force or not (RAW / f"{a}.png").exists()]
    print(f"{len(todo)} to generate, {jobs} parallel", flush=True)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for line in pool.map(gen, todo):
            print(line, flush=True)


if __name__ == "__main__":
    main()
