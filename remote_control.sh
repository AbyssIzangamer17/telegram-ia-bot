#!/bin/bash
# ================================================
# Script de Acceso Remoto - Tailscale + ngrok
# ================================================

set -e

REMOTE_DIR="/home/izan/.remote"
mkdir -p "$REMOTE_DIR"

show_menu() {
    clear
    echo "╔═══════════════════════════════════════════╗"
    echo "║     ACCESO REMOTO - Panel de Control        ║"
    echo "╠═══════════════════════════════════════════╣"
    echo "║  1. Instalar ambos (requiere sudo)       ║"
    echo "║  2. Iniciar Tailscale                 ║"
    echo "║  3. Iniciar ngrok                     ║"
    echo "║  4. Ver estado conexiones              ║"
    echo "║  5. Ver IP/hostname actual             ║"
    echo "║  6. Reiniciar bot Telegram            ║"
    echo "║  7. Conectar SSH remoto                ║"
    echo "║  8. Status completo                     ║"
    echo "║  0. Salir                              ║"
    echo "╚═══════════════════════════════════════════╝"
    echo ""
}

install_all() {
    echo "[*] Instalando Tailscale..."
    if ! command -v tailscale &> /dev/null; then
        curl -fsSL https://tailscale.com/install.sh | sh
    else
        echo "    [OK] Tailscale ya instalado"
    fi
    
    echo "[*] Instalando ngrok..."
    if ! command -v ngrok &> /dev/null; then
        cd "$REMOTE_DIR"
        wget -q https://bin.equinox.io/$(uname)/$(uname -m)/ngrok-stable-linux-amd64.zip
        unzip -o ngrok-stable-linux-amd64.zip
        sudo mv ngrok /usr/local/bin/
        rm ngrok-stable-linux-amd64.zip
        echo "    [OK] ngrok instalado"
    else
        echo "    [OK] ngrok ya instalado"
    fi
    
    echo ""
    echo "[*] Configurando servicios..."
    echo "[*] Ejecuta 'tailscale up --ssh' para activar"
    echo "[*] Ejecuta 'ngrok tcp 22' para SSH"
}

start_tailscale() {
    if command -v tailscale &> /dev/null; then
        echo "[*] Iniciando Tailscale..."
        tailscale up --ssh
    else
        echo "[!] Tailscale no instalado. Opción 1 para instalar."
    fi
}

start_ngrok() {
    if command -v ngrok &> /dev/null; then
        echo "[*] Iniciando ngrok SSH (puerto 22)..."
        echo "[*] Presiona Ctrl+C para detener"
        ngrok tcp 22 --region eu
    else
        echo "[!] ngrok no instalado. Opción 1 para instalar."
    fi
}

show_status() {
    echo "═════════ ESTADO ═════════"
    
    # Bot
    if pgrep -f "telegram_bot.py" > /dev/null; then
        echo "🤖 Bot Telegram: CORRIENDO (PID: $(pgrep -f telegram_bot.py | head -1))"
    else
        echo "🤖 Bot Telegram: DETENIDO"
    fi
    
    # Tailscale
    if command -v tailscale &> /dev/null; then
        if tailscale status 2>/dev/null | grep -q "Logged out"; then
            echo "🌐 Tailscale: DESCONECTADO"
        elif tailscale status 2>/dev/null | grep -q "online"; then
            echo "🌐 Tailscale: CONECTADO (IP: $(tailscale ip -4 2>/dev/null || echo '?'))"
        else
            echo "🌐 Tailscale: necesita 'tailscale up'"
        fi
    else
        echo "🌐 Tailscale: NO INSTALADO"
    fi
    
    # ngrok
    if command -v ngrok &> /dev/null; then
        echo "🔒 ngrok: disponible"
    else
        echo "🔒 ngrok: NO INSTALADO"
    fi
    
    echo "═══════════════════════"
}

show_ip() {
    echo "═════════ CONEXIONES ═════════"
    
    # IP pública
    echo "📡 IP Pública: $(curl -s ifconfig.me 2>/dev/null || echo 'No disponible')"
    
    # Tailscale
    if command -v tailscale &> /dev/null; then
        TS_IP=$(tailscale ip -4 2>/dev/null)
        if [ -n "$TS_IP" ]; then
            echo "🌐 Tailscale IP: $TS_IP"
            TS_HOST=$(tailscale status 2>/dev/null | grep -A1 "$(hostname)" | grep -oE '[a-zA-Z0-9-]+\.ts[a-z0-9]+\.net' | head -1)
            if [ -n "$TS_HOST" ]; then
                echo "🌐 Tailscale Host: $TS_HOST"
            fi
        fi
    fi
    
    echo "═══════════════════════"
}

restart_bot() {
    echo "[*] Reiniciando bot..."
    pkill -f telegram_bot.py 2>/dev/null || true
    sleep 1
    cd /home/izan
    nohup python3 telegram_bot.py > /tmp/bot.log 2>&1 &
    sleep 2
    if pgrep -f "telegram_bot.py" > /dev/null; then
        echo "[OK] Bot reiniciado"
    else
        echo "[!] Error al reiniciar. Ver /tmp/bot.log"
    fi
}

ssh_connect() {
    if command -v tailscale &> /dev/null; then
        TS_IP=$(tailscale ip -4 2>/dev/null)
        TS_HOST=$(tailscale status 2>/dev/null | grep -oE '[a-zA-Z0-9-]+\.ts[a-z0-9]+\.net' | head -1)
        
        if [ -n "$TS_HOST" ]; then
            echo "[*] Conectando a $TS_HOST..."
            echo "[*] Comando: ssh izan@$TS_HOST"
            ssh izan@$TS_HOST
        elif [ -n "$TS_IP" ]; then
            echo "[*] Conectando a $TS_IP..."
            ssh izan@$TS_IP
        else
            echo "[!] Tailscale no conectado"
        fi
    else
        echo "[!] Tailscale no instalado"
    fi
}

show_full_status() {
    show_status
    echo ""
    show_ip
    echo ""
    echo "═════════ SERVICIOS ═════════"
    ps aux | grep -E 'telegram_bot| tailscale' | grep -v grep || echo "Sin procesos activos"
    echo "═══════════════════════"
}

# Menu loop
while true; do
    show_menu
    read -p "Selecciona opción: " opt
    
    case $opt in
        1) install_all; read -p "Enter para continuar" ;;
        2) start_tailscale; read -p "Enter para continuar" ;;
        3) start_ngrok ;;
        4) show_status; read -p "Enter para continuar" ;;
        5) show_ip; read -p "Enter para continuar" ;;
        6) restart_bot; read -p "Enter para continuar" ;;
        7) ssh_connect ;;
        8) show_full_status; read -p "Enter para continuar" ;;
        0) exit 0 ;;
        *) echo "[!] Opción no válida" ;;
    esac
done