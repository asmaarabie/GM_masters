#! /bin/bash

cd square-3
count=20
for i in $(ls); do
	mv $i ../square-1/rep$count.csv
	let count=count+1
done
