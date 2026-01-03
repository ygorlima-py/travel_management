#!/usr/bin/env bash
set -euo pipefail

DATE="$(date +%Y%m%d_%H%M%S)"

PROJECT_DIR="$HOME/projects/travel_management"
BACKUP_DIR="$HOME/backups"

# Nome do serviço PostgreSQL no docker-compose
DB_SERVICE="psql"  # ✅ CORRIGIDO - conforme seu POSTGRES_HOST no .env

# Nome do banco e usuário conforme .env
DB_NAME="management_data_base"  # ✅ CORRIGIDO - POSTGRES_DB
DB_USER="management_user"       # ✅ CORRIGIDO - POSTGRES_USER

mkdir -p "$BACKUP_DIR"
cd "$PROJECT_DIR"

echo "📦 Fazendo backup do banco (Docker)..."
docker compose exec -T "$DB_SERVICE" pg_dump -U "$DB_USER" -d "$DB_NAME" -F c \
    > "$BACKUP_DIR/db_${DATE}.dump"

echo "🖼️  Fazendo backup das imagens (media)..."
tar -czf "$BACKUP_DIR/media_${DATE}.tar.gz" -C "$PROJECT_DIR" data/web/media/

echo "✅ Backup concluído:"
ls -lh "$BACKUP_DIR"/*"$DATE"*

# Limpeza: manter 7 dias
find "$BACKUP_DIR" -type f -name "db_*.dump" -mtime +7 -delete
find "$BACKUP_DIR" -type f -name "media_*.tar.gz" -mtime +7 -delete