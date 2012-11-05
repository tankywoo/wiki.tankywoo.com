for file in ./tkwiki/*.wiki
do
	vim -c Vimwiki2HTML -f +"wq" $file 
done
