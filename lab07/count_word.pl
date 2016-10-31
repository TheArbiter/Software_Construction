#!/usr/bin/perl -w

$total +=()= /\b\Q$ARGV[0]\E\b/gi for <STDIN>;
$word = lc $ARGV[0];
print "$word occurred $total times\n";
