#!/bin/bash
echo "Now will git pull codes from the remote"
echo "Enter (y/Y) to continue, others to exit :"
read input
if [ "$input" = "y" ] || [ "$input" = "Y" ]; then
	git pull
else
	exit 0
fi

echo "Git Pull is OK..."
