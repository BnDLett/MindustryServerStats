#!/bin/sh

PORT=$1
SCRIPT_PATH=$(dirname "$(realpath "$0")")
APP="mindustry_server_stats:app"

VENV_ALIAS="$SCRIPT_PATH/.venv/bin/python3"

alias venv=$VENV_ALIAS

cd "$SCRIPT_PATH" || (echo "Failed to start program." && exit)

if [ "$PORT" = '' ]
then
  PORT=8080
  echo "Port was not specified. Defaulting to $PORT"
fi

echo "Starting auto-updater job."
"$SCRIPT_PATH"/auto_updater.sh &

echo "Starting gunicorn."
#cd "$SCRIPT_PATH"/mindustry_server_stats || (echo "Failed to start." && kill "$(jobs -p)" && exit)

CORE_COUNT=$(nproc --all)

if [ -e server.crt ] && [ -e server.key ]
then
  venv -m gunicorn -w "$CORE_COUNT" "$APP" -b 0.0.0.0:"$PORT" --certfile=server.crt --keyfile=server.key --reload
else
  venv -m gunicorn -w "$CORE_COUNT" "$APP" -b 0.0.0.0:"$PORT" --reload
fi

kill "$(jobs -p)"

