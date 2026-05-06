#!/bin/bash
# Script para ejecutar el bot asegurando una sola instancia

LOCKFILE="/tmp/telegram_bot.lock"

# Verificar si ya hay una instancia corriendo
if [ -f "$LOCKFILE" ]; then
    PID=$(cat "$LOCKFILE" 2>/dev/null)
    if [ -n "$PID" ] && ps -p "$PID" > /dev/null 2>&1; then
        echo "El bot ya está corriendo (PID: $PID)"
        exit 1
    fi
fi

# Iniciar el bot
python3 /home/izan/telegram_bot.py &
BOTPID=$!
echo $BOTPID > "$LOCKFILE"

# Esperar a que termine
wait $BOTPID
rm -f "$LOCKFILE"
