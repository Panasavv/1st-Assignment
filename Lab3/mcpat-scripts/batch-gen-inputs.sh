#!/bin/bash

for RES_PATH in $(ls -d ../../Lab2/SPEC2006-design-exploration/spec*/)
do
	DEST_DIR=$(basename $RES_PATH)
	mkdir -p $DEST_DIR
	sh generate-mcpat-input.sh $RES_PATH inorder_arm.xml
	mv spec*.xml $DEST_DIR
done