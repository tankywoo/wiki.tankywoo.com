<!-- title : grep -->

grep [OPTIONS] PATTERN [FILE...]

grep [OPTIONS] [-e PATTERN | -f FILE] [FILE...]

egrep == grep -E

fgrep == grep -F

# Arguments #

` -e `
This can be used to specify multiple search patterns

` -f `
Obtain patterns from FILE, one per line.

` -i `
--ignore-case

` -v `
--invert-match

` -w `
--word-regexp

` -x `
--line-regexp

` -c `
print the match line number

` -m `

` -n `
print line number

` -r/-R `


# Examples #

	# The test.file is :
	root@gentoo-jl tmp # cat -n test.file
	     1  TankyWoo
	     2  tankywoo
	     3  tank
	     4  helloworld
	     5  say hello

	root@gentoo-jl tmp # grep -in 'tanky' test.file
	1:TankyWoo
	2:tankywoo

	root@gentoo-jl tmp # grep -in -e 'tanky' -e 'hello' test.file
	1:TankyWoo
	2:tankywoo
	4:helloworld
	5:say hello

	root@gentoo-jl tmp # grep -inv 'tanky' test.file
	3:tank
	4:helloworld
	5:say hello

	root@gentoo-jl tmp # grep -in -w 'sa' test.file
	root@gentoo-jl tmp # grep -in -w 'say' test.file
	5:say hello

	root@gentoo-jl tmp # grep -in -x 'say' test.file
	root@gentoo-jl tmp # grep -in -x 'say hello' test.file
	5:say hello

