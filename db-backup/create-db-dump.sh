#!/usr/bin/env bash
set -euxo pipefail

DUMP_FILE_NAME_BASENAME=$(basename -- "$DUMP_FILE_NAME")
DUMP_FILE_NAME_FULL_EXTENSION="${DUMP_FILE_NAME_BASENAME#*.}"

if [ $DUMP_FILE_NAME_FULL_EXTENSION = ".sql.gz" ]
then
    FORMAT_ARG="-Fp"
    DUMP_FILTER="gzip"
else
    FORMAT_ARG="-Fc"
    DUMP_FILTER="cat"
fi

DB_URI=$(echo $VCAP_SERVICES | jq -r '.postgres[0].credentials.uri')
echo -n "${PUBKEY}" > /app/public.key
gpg2 --import /app/public.key
pg_dump "${DB_URI}" -Fc --no-acl --no-owner --clean --if-exists $FORMAT_ARG | $DUMP_FILTER | \
  gpg2 --trust-model always -r "${RECIPIENT}" --out /app/"${DUMP_FILE_NAME}" --encrypt

/usr/local/bin/python /app/upload-dump-to-s3.py
