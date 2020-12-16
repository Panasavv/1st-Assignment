#!/bin/bash

for INPUT in $(find . -name spec*.xml | head -1)
do
	DEST_DIR=mcpat-results/$(basename $(dirname $INPUT))
	mkdir -p $DEST_DIR
	../../cmcpat/mcpat/mcpat -infile $INPUT -print_level 5 > $DEST_DIR/$(basename $INPUT).txt
done