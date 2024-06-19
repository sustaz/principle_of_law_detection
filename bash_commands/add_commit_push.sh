#!/bin/bash

cd principle_of_law_detection

# Add all changed files to the staging area
git add .

# Commit the changes with a message
git commit -m "$1"

# Push the changes to the remote repository
git push

cd ..