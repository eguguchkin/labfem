#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/v3/site"
DIST_DIR="$SCRIPT_DIR/dist"

echo "🏗️  Начало сборки..."

if [ -d "$DIST_DIR" ]; then
    rm -rf "$DIST_DIR"
    echo "🧹 Папка dist очищена"
fi
mkdir -p "$DIST_DIR"

crc32() {
    cksum "$1" | awk '{printf "%08x", $1}'
}

# Полный маппинг — для замены в HTML (пути вида assets/...)
MAPPING_FILE=$(mktemp)
# Маппинг картинок относительно assets/img/ — для замены url(...) внутри CSS
# (формат: "<sub>/<name.ext>:<sub>/<name>.<hash>.<ext>", sub может быть ".")
IMG_MAPPING_FILE=$(mktemp)
trap "rm -f $MAPPING_FILE $IMG_MAPPING_FILE" EXIT

IMG_DIR="assets/img"
CSS_DIR="assets/css"
JS_DIR="assets/js"

# ---------- 1) Картинки (первыми!) — включая вложенные директории ----------
# find обходит paint/, orn/, icon/, logo/, tex/, meta/ и любую глубину.
while IFS= read -r -d '' f; do
    rel="${f#"$SRC_DIR"/$IMG_DIR/}"              # путь внутри assets/img/, напр. paint/cycle-venus.webp
    filename=$(basename "$f")
    sub=$(dirname "$rel")                        # напр. paint, или . для корня
    hash=$(crc32 "$f")
    base="${filename%.*}"
    ext="${filename##*.}"
    src_rel="$IMG_DIR/$rel"
    new_rel="$sub/${base}.${hash}.${ext}"
    new_rel="${new_rel#./}"
    mkdir -p "$DIST_DIR/$IMG_DIR/$sub"
    cp "$f" "$DIST_DIR/$IMG_DIR/$new_rel"
    # для HTML: assets/img/paint/x.webp → assets/img/paint/x.<hash>.webp
    echo "$src_rel:$IMG_DIR/$new_rel" >> "$MAPPING_FILE"
    # для CSS: paint/x.webp → paint/x.<hash>.webp (url('../img/<old>') → url('../img/<new>'))
    echo "$rel:$new_rel" >> "$IMG_MAPPING_FILE"
    echo "✓ $src_rel → $IMG_DIR/$new_rel"
done < <(find "$SRC_DIR/$IMG_DIR" -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.svg' -o -name '*.webp' -o -name '*.gif' \) -print0 | sort -z)

# ---------- 2) CSS: сначала переписать url(), потом хешировать ----------
while IFS= read -r -d '' f; do
    filename=$(basename "$f")
    TMP_CSS=$(mktemp)
    cp "$f" "$TMP_CSS"

    # Подставляем <sub>/<old> → <sub>/<new> внутри '../img/...'.
    # Работает и для url("../img/paint/x.webp"), и для корневых ("../img/x.png").
    # Без sed -i (несовместим BSD/GNU): результат в новый файл, потом mv.
    while IFS=: read -r old_name new_name; do
        old_esc=$(printf '%s' "$old_name" | sed 's/\./\\./g')
        sed "s|img/${old_esc}|img/${new_name}|g" "$TMP_CSS" > "${TMP_CSS}.new"
        mv "${TMP_CSS}.new" "$TMP_CSS"
    done < "$IMG_MAPPING_FILE"

    hash=$(crc32 "$TMP_CSS")
    base="${filename%.*}"
    ext="${filename##*.}"
    src_rel="$CSS_DIR/$filename"
    dst_rel="$CSS_DIR/${base}.${hash}.${ext}"
    mkdir -p "$DIST_DIR/$CSS_DIR"
    cp "$TMP_CSS" "$DIST_DIR/$dst_rel"
    rm -f "$TMP_CSS"
    echo "$src_rel:$dst_rel" >> "$MAPPING_FILE"
    echo "✓ $src_rel → $dst_rel"
done < <(find "$SRC_DIR/$CSS_DIR" -maxdepth 1 -type f -name '*.css' -print0 | sort -z)

# ---------- 3) JS ----------
while IFS= read -r -d '' f; do
    filename=$(basename "$f")
    hash=$(crc32 "$f")
    base="${filename%.*}"
    ext="${filename##*.}"
    src_rel="$JS_DIR/$filename"
    dst_rel="$JS_DIR/${base}.${hash}.${ext}"
    mkdir -p "$DIST_DIR/$JS_DIR"
    cp "$f" "$DIST_DIR/$dst_rel"
    echo "$src_rel:$dst_rel" >> "$MAPPING_FILE"
    echo "✓ $src_rel → $dst_rel"
done < <(find "$SRC_DIR/$JS_DIR" -maxdepth 1 -type f -name '*.js' -print0 | sort -z)

# ---------- 4) HTML + замена ссылок ----------
while IFS= read -r -d '' html; do
    filename=$(basename "$html")
    cp "$html" "$DIST_DIR/$filename"

    # Замена ссылок — тоже без sed -i (переносимо BSD/GNU)
    while IFS=: read -r old_rel new_rel; do
        old_esc=$(printf '%s' "$old_rel" | sed 's/\./\\./g')
        sed "s|${old_esc}|${new_rel}|g" "$DIST_DIR/$filename" > "${DIST_DIR}/${filename}.new"
        mv "${DIST_DIR}/${filename}.new" "$DIST_DIR/$filename"
    done < "$MAPPING_FILE"

    echo "✓ Обновлены ссылки в $filename"
done < <(find "$SRC_DIR" -maxdepth 1 -type f -name '*.html' -print0 | sort -z)

find "$DIST_DIR" -type d -exec chmod 755 {} +
find "$DIST_DIR" -type f -exec chmod 644 {} +

echo ""
echo "✅ Сборка завершена! Результат в папке $DIST_DIR"
find "$DIST_DIR" -type f | sort
