#!/bin/bash

SOURCE_FILE=$1
DEST_DIR=$2
BACKUP_DATE=$3

# Function to perform the backup
perform_backup() {
    cp "$SOURCE_FILE" "$DEST_DIR"
    echo "Backup of $SOURCE_FILE to $DEST_DIR completed."
}

# Perform backup immediately
if [ "$BACKUP_DATE" == "now" ]; then
    perform_backup
    exit 0
fi

# Perform backup based on the date
if [[ "$BACKUP_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    CURRENT_DATE=$(date +%Y-%m-%d)
    if [ "$BACKUP_DATE" == "$CURRENT_DATE" ]; then
        perform_backup
        exit 0
    else
        echo "Scheduled backup for $BACKUP_DATE."
        exit 0
    fi
fi

# Perform backup based on the frequency (possible to use if Python not used for this)
# if [ "$BACKUP_DATE" == "daily" ]; then
#     perform_backup
#     exit 0
# fi

# if [ "$BACKUP_DATE" == "weekly" ]; then
#     perform_backup
#     exit 0
# fi

# if [ "$BACKUP_DATE" == "monthly" ]; then
#     perform_backup
#     exit 0
# fi

# If none of the conditions match, the backup is not scheduled
echo "Backup not scheduled."
exit 1
