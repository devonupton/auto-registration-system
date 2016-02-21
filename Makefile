# Ensure you are in the directory you want the directory "C291_project1" to
# appear before calling make.

make:
	echo "use make setup to run setup."

setup:
	git clone https://github.com/hreherch/C291_project1

recall:
	rm -f *
	git clone https://github.com/hreherch/C291_project1 ../C291_project1
	