source activate tools

REGEX='*.py'
DIR="src/hyperloop/Python src/hyperloop/Python/tests"
for y in $DIR; do
	for x in $y/*; do
		if [ -f $x ] && [[ $x =~ .*\.py$ ]] && ! [[ $x =~ .*__init__.py$ ]]; then
			echo $x
			git checkout master $x
			yapf -i $x
		fi
	done
done

