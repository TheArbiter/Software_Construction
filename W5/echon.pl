#!/usr/bin/perl -w

if (scalar @ARGV != 2) {
    print "Usage: ./echon.pl <number of lines> <string>\n";
}else{ 
    for ($n = $ARGV[0]; $n != 0; $n--) {  
        print "$ARGV[1]\n"; 
    }        
}
