#!/bin/bash
# @Tanky Woo
# manage the all script of the wiki

echo "Enter the number(1/2/3/4/0) to choose the operatration:"
#echo "--------------------------------"
#echo "| 1.Create a wiki file         |"
#echo "| 2.Update the wiki files      |"
#echo "| 3.Generate the html files    |"
#echo "| 4.Sync the files to Github   |"
#echo "--------------------------------"

# TODO????? can't use `xxx`
bash ./scripts/show.sh

while true
do
	read input
	case "$input" in
		1 | a | A ) bash ./scripts/create.sh;;
		2 | b | B ) bash ./scripts/update.sh;;
		3 | c | C ) bash ./scripts/generate_html.sh;;
		4 | d | D ) bash ./scripts/sync.sh;;
		0 ) flag=false;break;; 
	esac

	# $flag用来记录是否输入的是0
	echo $flag
	if [ "$flag" = "" ]; then
		#echo "haha"
		break
	fi

	echo "Do you want to continue(y/n)?"
	read yes_or_no
	case "$yes_or_no" in
		y | yes | Y ) bash ./scripts/show.sh;;
		n | no | N ) break;;
	esac
done

exit 0
