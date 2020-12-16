#!/bin/sh

for STAT in $(find $1 -name stats.txt)
do
	RES_DIR=$(dirname $STAT)
	JSON=$RES_DIR/config.json
	python2 GEM5ToMcPAT.py --out=$(echo $STAT | rev | cut -d '/' -f 2 | rev).xml $STAT $JSON $2
done