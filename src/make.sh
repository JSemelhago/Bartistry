#!/bin/bash

for file in $(find $src -name '*.py')
do
	python $file
done