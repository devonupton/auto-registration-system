# Ensure you are in the directory you want the directory "C291_project1" to
# appear before calling make.

# This makefile is designed to be in the directory above C291_project1

make:
	# Use 'make setup' to run setup.
	# This file is meant to be in the directory you want ./C291_project1 to appear.

# copies the Makefile into the above directory.

move: 	copy
copy:
	cp ./Makefile ../

# Creates a clone of the repository in the directory the Makefiel is in
setup:
	git clone https://github.com/hreherch/C291_project1

# Removes the repository from the working directory
	# WARNING!! DO NOT USE UNLESS YOU ARE SURE YOU WILL NOT LOSE DATA!!
remove:
	echo "Resetting your workspace..."
	rm -rf ./C291_project1

# Removes the repository from the working directory, but also begins to clone
# the repository again
	# WARNING!! DO NOT USE UNLESS YOU ARE SURE YOU WILL NOT LOSE DATA!!
recall: 
	make remove
	make setup
	echo "Done."