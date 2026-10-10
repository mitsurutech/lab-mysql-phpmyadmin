#!/usr/bin/env bash
# The table written before the containers were removed is still there: it lives in the
# named volume, which is what the platform saves.
set -euo pipefail
: "${NET:?run through test/check.sh}"
docker run --rm --network "$NET" lab-check-probe sh -c \
  'printf "[client]\nssl-verify-server-cert=0\n" > ~/.my.cnf; exec "$@"' sh mariadb -h db -u student -pstudent shop -N -e "SELECT COUNT(*) FROM fruit" | grep -qx 2
echo "  shop.fruit survived"
