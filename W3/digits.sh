#!/bin/sh

while read line
do
   echo $line | sed -e 's/[0-4]/</g' -e 's/[6-9]/>/g'
done 
