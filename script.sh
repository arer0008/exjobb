#!/bin/bash
FILES=Collea/*
for f in $FILES
do
	file=${f##*/}	
	echo "Processing $file file..."
	# Crop whitespaces.
	convert Collea/$file -flatten -fuzz 50% -median 2 -trim  Collea/converted/$file
done
