#! /bin/bash
# sync.sh

git status

echo "Input y/Y to continue sync to github, others to exit"
read input

if [ "$input" = "y" ] || [ "$input" = "Y" ]; then
	continue
else
	exit 0
fi


TIME=`date '+%F %T'`

# add all new files
git add .
# TODO change to input the message by hand
git commit -a -m "auto commit at $TIME"

# push to server
git push

