#! /bin/bash

# This script is used to automate the Git push process

# Get the current branch name
branch=$(git branch --show-current)

# Add all changes to the staging area
git add .

# Get the commit message
# If the commit message is blank, use the auto-summary
echo "Enter the commit message (leave blank for auto-summary): "

read -p "Commit message (leave blank for auto-summary): " commit_msg
if [ -z "$commit_msg" ]; then
  summary=$(git diff --cached --name-only | tr '\n' ', ' | sed 's/, $//')
  commit_msg="Update: ${summary:-no file changes detected}"
fi

git commit -m "$commit_msg"
git push origin "$branch"

# Print the result
echo "Changes pushed to the remote repository"


# Exit the script
exit 0


