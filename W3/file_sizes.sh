#!/bin/sh

small="Small files: "
medium="Medium-sized files: "
large="Large files: "

for x in *
do
   line=`wc -l $x | cut -d' ' -f1`
   
   if [ $line -lt 10 ]
   then
      small="$small $x"
   elif [ $line -lt 100 ]
   then
      medium="$medium $x"
   else 
      large="$large $x"
   fi
done

echo $small
echo $medium
echo $large
