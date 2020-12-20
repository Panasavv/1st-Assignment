#! /bin/bash

for DATA_DIR in $(ls -d ../mcpat-results-SPEC2006/spec*)
do
	BENCHMARK_NAME=$(basename $DATA_DIR)
	mkdir -p $BENCHMARK_NAME
	python3 make-graphs.py $DATA_DIR/$BENCHMARK_NAME\_core.csv $DATA_DIR/$BENCHMARK_NAME\_l2.csv $DATA_DIR/time_${BENCHMARK_NAME#spec}.txt $BENCHMARK_NAME
	mv $BENCHMARK_NAME-* $BENCHMARK_NAME
done