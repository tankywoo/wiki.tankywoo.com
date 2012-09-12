#! /bin/sh
TIME=`date`

# add all new files
git add .
git commit -m 'Automated commit on $TIME'

# push to server
git push
