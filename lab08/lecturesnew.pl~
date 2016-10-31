#!/usr/bin/perl -w

my $flag = shift @ARGV if $ARGV[0] =~ /-d/;
my ($last, $details) = 0;
my @content;

for my $course (@ARGV) {
   my $url_base = "http://www.timetable.unsw.edu.au/current/$course.html";
   my $time_table = `wget -q -O- $url_base`;    
   while ($time_table =~ /Lecture[^<]*?<\/a>.*?([SX][12])(.*?<td class=){5}.*?>([^<]*?)</sg and $3) {
      $details = "$course: $1 $3\n";
      my $semester = $1;
      if (defined $flag and $details ne $last) {
         push @content, $details =~ /([MTWFS]\w\w)0?(\d+):\d+\s-\s0?(\d+):(\d+)\s/g;
         push @content, $details =~ /([MTWFS]\w\w)\s0?(\d+):\d+\s-\s0?(\d+):(\d+)\s/g;
         while (@content) {
            if($content[3] == 0){
               print "$semester $course $content[0] ",$content[1]++,"\n" while ($content[1] < $content[2]);
               shift @content for (1..4);
            } else {
               print "$semester $course $content[0] ",$content[1]++,"\n" while ($content[1] <= $content[2]);
               shift @content for (1..4);
            }
        }
      } else {
         print $details if $details ne $last;
      }
         $last = $details;
   }
}
