#!/bin/bash 

if [ $# != 2 ]
then
    echo 'Usage: ./echon.sh <number of lines> <string>'
    exit 1
elif ! [[ $1 =~ ^[0-9]+$ ]]
then
    echo "$0: argument 1 must be a non-negative integer"
    exit 1     
else
    for (n=0;n < $1;n++)
    do
        echo "$2"
    done
fi
