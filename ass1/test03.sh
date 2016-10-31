#!/bin/bash

a=1

while [ $a -le 5 ]
do
echo "Hello $a times"
((a++))
done
