#!/bin/sh

x=`wget -q -O- "http://www.handbook.unsw.edu.au/vbook2015/brCoursesByAtoZ.jsp?StudyLevel=Undergraduate&descr=all"`
y=`wget -q -O- "http://www.handbook.unsw.edu.au/vbook2015/brCoursesByAtoZ.jsp?StudyLevel=Postgraduate&descr=ALL"`

echo "$x\n$y"| grep "2015/$1" | sed -e 's/<TD class\=\"\"><A href="http\:\/\/www\.handbook\.unsw\.edu\.au\/undergraduate\/courses\/2015\///g' -e 's/\.html\">//g' -e 's/\s*<\/A><\/TD>//g' -e 's/<TD class\=\"evenTableCell\"><A href\=\"http\:\/\/www\.handbook\.unsw\.edu\.au\/undergraduate\/courses\/2015\///g' | sed -e 's/<TD class\=\"\"><A href="http\:\/\/www\.handbook\.unsw\.edu\.au\/postgraduate\/courses\/2015\///g' -e 's/\.html\">//g' -e 's/\s*<\/A><\/TD>//g' -e 's/<TD class\=\"evenTableCell\"><A href\=\"http\:\/\/www\.handbook\.unsw\.edu\.au\/postgraduate\/courses\/2015\///g' | cut -f9 | sort | uniq | sed 's/[0-9][0-9][0-9][0-9]/& /g'
