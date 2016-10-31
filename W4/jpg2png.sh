#!/bin/bash

for x in *.jpg
do
   if test -f "`echo "$x" | sed s/.jpg/.png/g`"
   then
      echo "`echo "$x" | sed s/.jpg/.png/g` already exists"
      exit 1
   else   
     convert "`echo "$x"`" "`echo "$x" | sed s/.jpg/.png/g`"   
   rm -r "$x"
   fi   
done

