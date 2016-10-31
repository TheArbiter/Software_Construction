#!/usr/bin/perl -w

$num = 0;
$count = 0;

@whales = ();
my %current_count;
my %pod_sum;

while ($line = <STDIN>) {
   if ($line =~ /(\d+)\s*(.+)\s*$/i){
      $num = $1;
      $name = lc $2;
      $name =~ s/\s+$//;
      $name =~ s/\h+/ /;
      $name =~ s/s$//;
      
      if (!exists $pod_sum{$name}){
         $pod_sum{$name} = 0;
         $current_count{$name} = 0;
         $whales[$count] = $name;
         $count++;   
      }
      $pod_sum{$name}++;
      $current_count{$name} += $num;
   }
}

@whales = sort @whales;

foreach $whale(@whales){
   print "$whale observations:  $pod_sum{$whale} pods, $current_count{$whale} individuals\n";
}   
