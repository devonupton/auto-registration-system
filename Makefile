# Ensure you are in the directory you want the directory "C291_project1" to
# appear before calling make.

# This makefile is designed to be in the directory above C291_project1

make:
	#echo "Use 'make' setup to run setup."
	#echo -e "This file is meant to be in the directory you want ./C291_project1 \nto appear."

move:
	mv ./Makefile ../

setup:
	git clone https://github.com/hreherch/C291_project1

remove:
	echo "Resetting your workspace..."
	rm -rf ./C291_project1

recall: remove, setup
	echo "Done."