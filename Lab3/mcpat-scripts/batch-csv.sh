#! /bin/bash

for DIR in $(ls -d ../mcpat-results-SPEC2006/spec*/)
do
	python3 mcpat-to-csv.py $DIR
	mv results_core.csv $(basename $DIR)_core.csv
	mv results_l2.csv $(basename $DIR)_l2.csv
done