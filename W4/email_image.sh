#!/bin/bash

for x in "$@"
do
   display "$x"
   read -p "Address to e-mail this image to? " email
   if test -n $email
   then
      read -p "Message to accompany image? " message
      echo "$message"| mutt -s "$x" -a "$x" -- "$email"
      echo ""$x" sent to "$email""
   fi
done
