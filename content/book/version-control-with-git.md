---
title: "Version Control with Git"
date: 2014-04-28 23:31
---

[TOC]


## 8. Diffs ##

four fundamental comparisons:

`git diff` : between working directory and the index.

`git diff <commit>` : between working directory and the given commit.

`git diff --cached <commit>` : between the staged changes in the index and the given commit. `--staged` is the new synonym of `--cached`.

`git diff <commit1> <commit2>` : between the arbitrary two commits.

Options:

`-M` : #todo#

> The --M option detects renames and generates a simplified output that simply re- cords the file rename rather than the complete removal and subsequent addition of the source file. If the rename is not a pure rename but also has some additional content changes, Git calls those out.

`-w` or `--ignore-all-space`: compare without considering changes in whitespace as significant.

`--stat` : show statistics about the difference between any two tree states.

git diff with Path Limiting:

	# limit changes in specify directory
	git diff some_directory

	# limit changes in specify file
	git diff some_file

search changes containing string with `-S`:

	# search the past 50 commits to the master branch for changes containing string "octopus"
	git diff -S "octopus" master~50

