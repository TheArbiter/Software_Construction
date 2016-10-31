#!/usr/bin/perl -w


@lines = <>;

while (@lines){
   print splice(@lines,int(rand(@lines)) ,1);
}
