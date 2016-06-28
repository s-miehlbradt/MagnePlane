
REGEX='*.py'
for x in src/hyperloop/Python/*; do
	if [ -f $x ] && [[ $x =~ .*\.py$ ]] && ! [[ $x =~ ^__ ]]; then
		echo $x
	fi
done