#!/bin/bash
# @Tanky Woo

# Show the input information
function Show()
{
	echo ''
	echo "-------------------------------"
	echo "| 1.Create a wiki file        |"
	echo "| 2.Update the wiki files     |"
	echo "| 3.Generate the html files   |"
	echo "| 4.Sync the files to Github  |"
	echo "| 0.Exit                      |"
	echo "-------------------------------"
	echo "Enter the number(1/2/3/4/0) to choose the operatration:"
}

# Create the wiki file
function Create()
{
	echo "Enter the wiki file's name:"
	read filename

	vim ./tkwiki/"$filename.wiki"
}

# Use git pull to update wiki project
function Update()
{
	echo "Now will git pull codes from the remote"
	echo "Enter (y/Y) to continue, others to exit :"
	read input
	if [ "$input" = "y" ] || [ "$input" = "Y" ]; then
		git pull
		echo "Git Pull is OK..."
	else
		:
		#return
	fi
}

# Batch generate html file from .wiki
function Generate()
{
	for file in ./tkwiki/*.wiki
	do
		vim -c Vimwiki2HTML -f +"wq" $file
	done
}

# Sync the wiki project to github
function Sync()
{
	git status

	echo "Input y/Y to continue sync to github, others to exit"
	read input

	if [ "$input" = "y" ] || [ "$input" = "Y" ]; then
		git add .
	else
		return
	fi

	TIME=`date '+%F %T'`

	echo 'Input the commit message'
	read commit_msg
	# XXX
	if [[ $commit_msg ]]; then
		git commit -a -m "$commit_msg @ $TIME"
	else
		git commit -a -m "auto commit @ $TIME"
	fi

	# push to server
	git push
}


# Main Entry
Show

while true
do
	read input
	case "$input" in
		1 | a | A ) Create ;;
		2 | b | B ) Update ;;
		3 | c | C ) Generate ;;
		4 | d | D ) Sync ;;
		0 ) flag=false; break ;; 
	esac

	echo "Do you want to continue(y/n)?"
	read yes_or_no
	case "$yes_or_no" in
		y | yes | Y ) Show;;
		n | no | N ) break;;
	esac
done

exit 0
