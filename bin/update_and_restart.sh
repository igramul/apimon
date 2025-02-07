#!/bin/bash

REPO_DIR="."
LAST_COMMIT_FILE="$REPO_DIR/.last_commit.txt"

cd $REPO_DIR || exit

git pull

# git current commit id
CURRENT_COMMIT=$(git rev-parse HEAD)

# check if file with last git commit exists
if [[ ! -f $LAST_COMMIT_FILE ]]; then
    # If not, create the file and save the current commit ID
    echo "$CURRENT_COMMIT" > $LAST_COMMIT_FILE
    echo "Initial execution: current commit ID saved."
else
    # read last saved commit-ID
    LAST_COMMIT=$(cat $LAST_COMMIT_FILE)

    # Compare the current commit ID with the last saved one
    if [[ "$CURRENT_COMMIT" != "$LAST_COMMIT" ]]; then
        echo "Change found. Local git repo updated. Going to restart service."

        sudo systemctl restart apimon.service

        # Update the saved commit ID
        echo "$CURRENT_COMMIT" > $LAST_COMMIT_FILE
    else
        echo "No change in the repository."
    fi
fi
