#!/usr/bin/perl -w

$current_count = 0;
$pod_sum = 0;

if (@ARGV != 1){
   die;
}

while ($line = <STDIN>) {
   if ($line =~ /(\d+)\s$ARGV[0]/){
      $pod_sum++;
      $current_count += $1;
   }
}

print "$ARGV[0] observations: $pod_sum pods, $current_count individuals\n";
