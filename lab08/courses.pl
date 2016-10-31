#!/usr/bin/perl -w

$url_base = "http://www.timetable.unsw.edu.au/current/$ARGV[0]KENS.html";
foreach $course (@ARGV) {
   open F, "wget -q -O- $url_base|" or die;
   while ($line = <F>) {      
       if ($line =~ m/<a href="[A-Z]{4}\d{4}.html">/i){
         $line =~ s/\s*<[^>]*>\s*//g;
         my @courses = $line =~ /([A-Z]{4}\d{4})/g;
         push @list, @courses;
      }
   }
}
foreach $course (sort @list){
   print "$course\n";
}
