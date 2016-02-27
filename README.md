# C291_project1
### git and github tips

###### Setup:
git clone https://github.com/hreherch/C291_project1
>	This will create a new directory called "C291_project1" where
>	you call this command

git config --global core.editor "[your editor] -w"	
>	This will set your text editor to your choice (might need to
>	specify the exact location) and the -w command tell git to
>	wait before trying to commit (you will need to close the
>	commit file in the text editor before being able to commit).

###### Commands:
git branch
>	List all the avaliable branches in this project
		
git branch [branch-name]
>	Creates a new branch based on this name from the current directory
		
git checkout [branch-name]
>	Loads all data from that branch and makes this your current workingspace
		
git commit -a
>	Creates a commit for all the new changes in data in the branch 
		
git add [filename]
>	Adds a file to tracked when commits are made
		
git merge [branch/master name]
>	Merges the requested branch into the currently checked out branch
>	USEFUL TO AVOID CONFLICTS WHEN MERGING BEFORE MERGING INTO MASTER...

git remote prune origin 
> 	Removes old and stale branches (use --dry-run to prevent fuckups)
