#!/bin/sh
set -e

# Restore the database
litestream restore -v -if-replica-exists -o ./db.sqlite ${DB_REPLICA_REMOTE_PATH}

if [ -f ./db.sqlite ]; then
    echo "---- Restored from Cloud Storage ----"
else
    echo "---- Failed to restore from Cloud Storage ----"
    flask db init
    flask db migrate
    flask db upgrade
fi

# Run litestream with your app as the subprocess.
exec litestream replicate -exec "flask run -h 0.0.0.0" ./db.sqlite ${DB_REPLICA_REMOTE_PATH} 