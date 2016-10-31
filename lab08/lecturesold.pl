#!/usr/bin/perl -w

for my $course (@ARGV) {
    my $url = "http://www.timetable.unsw.edu.au/current/$course.html";
    my $time_table = `wget -q -O- $url`;
    while ($time_table =~ /(?=Lecture).*?T([12])(.*?<td){5}.*?>(.*?)</sg and $3){
      print "$course: S$1 $3\n" 
    }
}
