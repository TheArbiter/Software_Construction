#!/usr/bin/perl

# written by andrewt@cse.unsw.edu.au August 2015
# as a starting point for COMP2041/9041 assignment 
# http://cgi.cse.unsw.edu.au/~cs2041/assignment/shpy

#Edited by Ryan Shivashankar on the 7th September 2015

$count = 0;
while ($line = <>) {
   chomp $line;
   if ($line =~ /^#!/ && $. == 1) {
      print "#!/usr/bin/python2.7 -u\n";
   } elsif ($line =~ /echo /) {
      $line=~ s/echo //;
      if($line=~ /\$/){
         $line=~ s/\$//;
         $line=~ s/\$//;
         $line=~ s/ /, /;
         my @ech = split /echo /,$line;
         print "print @ech\n";
      } else {
         $line=~ s/ /','/g;
         my @ech = split /echo /,$line;
         print "print '@ech'\n";
      }
   } elsif ($line =~ /=/) {
      $line=~ s/=/ /;
      $line=~ s/ / = '/;
      $line=~ s/$/'\$/;
      $line=~ s/\$//;
      print "$line\n";
   }else {
      # Lines we can't translate are turned into comments
      print "import subprocess\n" if(($line =~ /ls||pwd/) && $count == 0);
      $count = 1;
      my $str = $line;
      chomp $str;
      $line=~ s/ /', '/g;
      my @fields = split / /,$line;
      print "subprocess.call(['@fields'])\n";
      #print "#$line\n";
   }

}
