#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/site"
DIST_DIR="$SCRIPT_DIR/dist"

echo "🏗️  Начало сборки..."

if [ -d "$DIST_DIR" ]; then
    rm -rf "$DIST_DIR"
    echo "🧹 Папка dist очищена"
fi
mkdir -p "$DIST_DIR/assets/css"
mkdir -p "$DIST_DIR/assets/js"
mkdir -p "$DIST_DIR/assets/img"

crc32() {
    cksum "$1" | awk '{printf "%08x", $1}'
}

# Полный маппинг — для замены в HTML (пути вида assets/...)
MAPPING_FILE=$(mktemp)
# Маппинг картинок — для замены url(...) внутри CSS
IMG_MAPPING_FILE=$(mktemp)
trap "rm -f $MAPPING_FILE $IMG_MAPPING_FILE" EXIT

shopt -s nullglob

# ---------- 1) Картинки (первыми!) ----------
IMG_DIR="assets/img"
for f in "$SRC_DIR"/$IMG_DIR/*.{png,jpg,jpeg,svg,webp,gif}; do
    if [[ -f "$f" ]]; then
        filename=$(basename "$f")
        hash=$(crc32 "$f")
        base="${filename%.*}"
        ext="${filename##*.}"
        src_name="$IMG_DIR/$filename"
        dst_name="$IMG_DIR/${base}.${hash}.${ext}"
        cp "$f" "$DIST_DIR/$dst_name"
        # для HTML
        echo "$src_name:$dst_name" >> "$MAPPING_FILE"
        # для CSS (без префикса assets/)
        echo "$filename:${base}.${hash}.${ext}" >> "$IMG_MAPPING_FILE"
        echo "✓ $f → $dst_name"
    fi
done

# ---------- 2) CSS: сначала переписать url(), потом хешировать ----------
CSS_DIR="assets/css"
for f in "$SRC_DIR"/$CSS_DIR/*.css; do
    if [[ -f "$f" ]]; then
        filename=$(basename "$f")
        TMP_CSS=$(mktemp)
        cp "$f" "$TMP_CSS"

        # Подставляем img/<old> → img/<new>.
        # Работает и для url("../img/foo.webp"), и для url("assets/img/foo.webp").
        while IFS=: read -r old_name new_name; do
            old_esc=$(echo "$old_name" | sed 's/\./\\./g')
            sed -i '' "s|img/${old_esc}|img/${new_name}|g" "$TMP_CSS"
        done < "$IMG_MAPPING_FILE"

        hash=$(crc32 "$TMP_CSS")
        base="${filename%.*}"
        ext="${filename##*.}"
        src_name="$CSS_DIR/$filename"
        dst_name="$CSS_DIR/${base}.${hash}.${ext}"
        cp "$TMP_CSS" "$DIST_DIR/$dst_name"
        rm -f "$TMP_CSS"
        echo "$src_name:$dst_name" >> "$MAPPING_FILE"
        echo "✓ $f → $dst_name"
    fi
done

# ---------- 3) JS ----------
JS_DIR="assets/js"
for f in "$SRC_DIR"/$JS_DIR/*.js; do
    if [[ -f "$f" ]]; then
        filename=$(basename "$f")
        hash=$(crc32 "$f")
        base="${filename%.*}"
        ext="${filename##*.}"
        src_name="$JS_DIR/$filename"
        dst_name="$JS_DIR/${base}.${hash}.${ext}"
        cp "$f" "$DIST_DIR/$dst_name"
        echo "$src_name:$dst_name" >> "$MAPPING_FILE"
        echo "✓ $f → $dst_name"
    fi
done

shopt -u nullglob

# ---------- 4) HTML + замена ссылок ----------
for html in "$SRC_DIR"/*.html; do
    if [[ -f "$html" ]]; then
        filename=$(basename "$html")
        cp "$html" "$DIST_DIR/$filename"

        while IFS=: read -r old_name new_path; do
            old_escaped=$(echo "$old_name" | sed 's/\./\\./g')
            sed -i '' "s|${old_escaped}|${new_path}|g" "$DIST_DIR/$filename"
        done < "$MAPPING_FILE"

        echo "✓ Обновлены ссылки в $filename"
    fi
done

find "$DIST_DIR" -type d -exec chmod 755 {} +
find "$DIST_DIR" -type f -exec chmod 644 {} +

echo ""
echo "✅ Сборка завершена! Результат в папке $DIST_DIR"
find "$DIST_DIR" -type f