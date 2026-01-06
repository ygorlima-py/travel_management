#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/vars.sh"

DATE="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$BACKUP_DIR"
cd "$PROJECT_DIR"

echo "📦 Fazendo backup do banco (Docker)..."
docker compose exec -T "$DB_SERVICE" pg_dump -U "$DB_USER" -d "$DB_NAME" -F c \
    > "$BACKUP_DIR/db_${DATE}.dump"

echo "🖼️  Fazendo backup das imagens (media)..."
tar -czf "$BACKUP_DIR/media_${DATE}.tar.gz" -C "$PROJECT_DIR" data/web/media/

echo "✅ Backup concluído:"
ls -lh "$BACKUP_DIR"/*"$DATE"*

# Limpeza: manter 3 dias
find "$BACKUP_DIR" -type f -name "db_*.dump" -mtime +3 -delete
find "$BACKUP_DIR" -type f -name "media_*.tar.gz" -mtime +3 -delete


VENV_PY="$PROJECT_DIR/venv/bin/python"

cd "$PROJECT_DIR"

echo ✅ Fazendo autentificação"
"$VENV_PY" "$PROJECT_DIR/backup/auth.py"

echo ✅ Comprimindo e enviando backup"
"$VENV_PY" "$PROJECT_DIR/backup/compress_file.py"