#!/bin/bash

SOURCE_FILE=$1
DEST_DIR=$2
BACKUP_DATE=$3

# Function to perform the backup
perform_backup() {
    cp "$SOURCE_FILE" "$DEST_DIR"
    echo "Backup of $SOURCE_FILE to $DEST_DIR completed."
}

if [ "$BACKUP_DATE" == "now" ]; then
    perform_backup
else
    # Schedule the backup using 'at'
    echo "cp \"$SOURCE_FILE\" \"$DEST_DIR\"" | at $BACKUP_DATE
    echo "Backup of $SOURCE_FILE to $DEST_DIR scheduled for $BACKUP_DATE."
fi
