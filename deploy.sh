#!/bin/bash
# Скрипт деплоя сайта на хостинг через rsync по SSH
# Деплоит содержимое папки dist/
# Исключает служебные файлы

set -e

# === КОНФИГУРАЦИЯ ===
# Замените эти значения на ваши данные
HOST="${DEPLOY_HOST:-labfem_ru_usr@labfem.ru}"
DEST_PATH="${DEPLOY_DEST:-www/labfem.ru/}"
SSH_PORT="${SSH_PORT:-22}"

# Файлы и папки для исключения
EXCLUDES=(
    ".git"
    ".gitignore"
    ".DS_Store"
    "*.log"
)

# === ОСНОВНАЯ ЧАСТЬ ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/dist"

# Проверяем наличие dist/
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ Ошибка: папка dist/ не найдена. Запустите 'make build' перед деплоем."
    exit 1
fi

# Формируем строку исключений для rsync
RSYNC_EXCLUDES=""
for exclude in "${EXCLUDES[@]}"; do
    RSYNC_EXCLUDES="$RSYNC_EXCLUDES --exclude='$exclude'"
done

echo "🚀 Деплой на $HOST:$DEST_PATH"
echo "Источник: $SOURCE_DIR"
echo "Исключаемые файлы/папки: ${EXCLUDES[*]}"
echo ""

# Проверяем наличие rsync
if ! command -v rsync &> /dev/null; then
    echo "❌ Ошибка: rsync не найден. Установите его:"
    echo "   Ubuntu/Debian: sudo apt install rsync"
    echo "   macOS: brew install rsync"
    exit 1
fi

# Создаем временный файл со списком исключений
EXCLUDE_FILE=$(mktemp)
printf '%s\n' "${EXCLUDES[@]}" > "$EXCLUDE_FILE"

# Создаём мастер-соединение (оно будет висеть в фоне)
SSH_OPTS="-o ControlMaster=auto -o ControlPath=/tmp/ssh-mux-%r@%h:%p -o ControlPersist=10"

# Выполняем rsync
# -a: архивный режим (сохраняет права, даты, симлинки)
# -v: подробный вывод
# -z: сжатие при передаче
# -P: показывает прогресс и позволяет возобновить прерванную передачу
# --delete: удаляет на сервере файлы, которых нет локально (опционально)
# --exclude-from: читает список исключений из файла

rsync -avzP --delete \
    --exclude-from="$EXCLUDE_FILE" \
    -e "ssh -p $SSH_PORT $SSH_OPTS" \
    "$SOURCE_DIR/" \
    "$HOST:$DEST_PATH"

# Удаляем временный файл
rm -f "$EXCLUDE_FILE"

echo ""
echo "✅ Деплой завершен!"
