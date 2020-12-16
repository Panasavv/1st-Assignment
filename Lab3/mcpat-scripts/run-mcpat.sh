#!/bin/bash

for INPUT in $(find . -name spec*.xml)
do
	echo $INPUT
	DEST_DIR=mcpat-results/$(basename $(dirname $INPUT))
	mkdir -p $DEST_DIR
	$1/mcpat -infile $INPUT -print_level 5 > $DEST_DIR/$(basename $INPUT).txt
done
