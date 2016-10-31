#!/usr/bin/perl -w


$num = 10;

if (@ARGV+0 and $ARGV[0] =~ /^-(\d+)$/) {
   $num = $1;
   shift @ARGV;
}

if (@ARGV+0 == 0){
   push @lines, <>;
   print @lines[-$num..-1];
} else {
   foreach $f (@ARGV) {
      open($F,"<",$f) or die "$0: Can't open $f: $!\n";
      print "==> $f <==\n" if ($#ARGV >= 1);
      push @lines, <$F>;
      
      if ($num < @lines){
         print @lines[-$num..-1];
      } else {
         print @lines;
      }  
   }
}

