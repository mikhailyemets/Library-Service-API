#!/usr/bin/env bash
set -e

HOST=$1
shift
PORT=$1
shift

until nc -z "$HOST" "$PORT"; do
  echo "Waiting for $HOST:$PORT..."
  sleep 2
done

exec "$@"
