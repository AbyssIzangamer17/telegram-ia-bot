#!/bin/bash
# Script de configuración de acceso remoto
# Ejecutar con: sudo bash setup_remote.sh

set -e

echo "==================================="
echo " Configuración de Acceso Remoto"
echo "==================================="

# 1. Instalar Tailscale
echo "[1/4] Instalando Tailscale..."
if ! command -v tailscale &> /dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
else
    echo "  Tailscale ya instalado"
fi

# 2. Verificar estado del bot
echo "[2/4] Verificando bot de Telegram..."
if pgrep -f "telegram_bot.py" > /dev/null; then
    echo "  Bot corriendo"
else
    echo "  Iniciando bot..."
    cd /home/izan
    nohup python3 telegram_bot.py > /tmp/bot.log 2>&1 &
fi

# 3. Configurar Tailscale
echo "[3/4] Configurando Tailscale..."
echo ""
echo "==================================="
echo " INSTRUCCIONES:"
echo "1. Ejecuta: tailscale up --ssh"
echo "2. Abre el enlace OAuth que aparecerá"
echo "3. Autentícate con tu cuenta Google/GitHub"
echo "4. Anota tu hostname de Tailscale"
echo "==================================="
echo ""

tailscale status || true

echo ""
echo "[4/4] Estado del sistema:"
echo "  - IP Tailscale: $(tailscale ip -4 2>/dev/null || echo 'pendiente')"
echo "  - Bot PID: $(pgrep -f telegram_bot.py | head -1 || echo 'no corriendo')"