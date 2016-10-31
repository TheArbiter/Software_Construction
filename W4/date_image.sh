#!/bin/bash

for x in "$@"
do

   date=`date -r "$x" +"%Y%m%d%H%M.%S"` 
   tag=`date -r "$x" | egrep -o '[A-Z][a-z]{2} [0-9]+ [0-9]{2}:[0-9]{2}'`
   convert -gravity south -pointsize 36 -annotate 0 "$tag" "$x" "$x"
   
   touch -t "$date" "$x"
   display $x
done
