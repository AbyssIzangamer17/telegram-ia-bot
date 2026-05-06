#!/bin/bash
# Script para subir todo el proyecto a GitHub
# Uso: ./push_to_github.sh <tu_token_github>

if [ -z "$1" ]; then
    echo "Uso: $0 <github_personal_access_token>"
    echo "Genera un token en: https://github.com/settings/tokens"
    exit 1
fi

TOKEN="$1"
REPO="AbyssIzangamer17/IA-TELEGRAM-BOT"

echo "Configurando acceso a GitHub..."
cd /home/izan

# Configurar Git si no está hecho
git config user.name "Izan" 2>/dev/null
git config user.email "izan@users.noreply.github.com" 2>/dev/null

# Cambiar URL remota con token
git remote set-url origin "https://${TOKEN}@github.com/${REPO}.git"

echo "Subiendo archivos a GitHub..."
git push -u origin main 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡ÉXITO! Repositorio subido correctamente:"
    echo "   https://github.com/${REPO}"
    echo ""
    echo "Archivos subidos:"
    echo "  - README.md (documentación principal)"
    echo "  - TECHNICAL_MEMORY.md (memoria técnica)"
    echo "  - PRODUCTION_AUDIT_REPORT.md (auditoría)"
    echo "  - docs/adr/ (Architecture Decision Records)"
    echo "  - .env.example (template de configuración)"
    echo "  - .gitignore (archivos ignorados)"
    echo ""
else
    echo ""
    echo "❌ Error al subir. Verifica:"
    echo "  1. El token tiene permiso 'repo'?"
    echo "  2. El repo existe en GitHub?"
    echo "  3. El token está bien copiado?"
    echo ""
    echo "Puedes probar también con:"
    echo "  curl -H 'Authorization: token ${TOKEN}' https://api.github.com/repos/${REPO}"
fi
