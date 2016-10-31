#!/bin/bash

a=10
b=20
c=5
d=5

if [ $a == $b ]
then
      echo a is equal to b
else
   if [ $d == $c ]
   then
      echo a is not equal to b and d is equal to c
   else
      echo a is not equal to b
   fi
fi
