#!/bin/bash

function make() {
	cmd="echo -n \"$1\" | ../humon/build/static_lib.gnu.debug/bin/hux -$3 -$4 -o tests/$2-$3-$4.hu"
	echo $cmd
	eval $cmd
}

function make_f() {
	cmd="../humon/build/static_lib.gnu.debug/bin/hux -i tests/$1.hu -$2 -$3 -o tests/$1-$2-$3.hu"
	echo $cmd
	eval $cmd
}

pvals=("pp" "pm" "pc")
cvals=("ca" "cn")
inps=("" "// snark" "@ foo: bar" "dreams" "[]" "{}")
names=("inane" "comment-only" "metatag-only" "value-only" "list-only" "dict-only")

len=${#names[@]}
for ((i=0; i<len; i++)); do
	for pval in "${pvals[@]}"; do
		for cval in "${cvals[@]}"; do
			make "${inps[i]}" "${names[i]}" $pval $cval
		done
	done
done

for pval in "${pvals[@]}"; do
	for cval in "${cvals[@]}"; do
		make_f "gnome" $pval $cval
	done
done
