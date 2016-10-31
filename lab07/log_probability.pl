#!/usr/bin/perl -w

foreach my $files (glob "poets/*.txt"){
   my ($total_words,$word_count,$add);
   open (F, "<", $files) or die "$0: $files: $!\n";
   foreach(<F>){
      $total_words +=()= /[A-Z]+/gi;
      $word_count +=()= /\b\Q$ARGV[0]\E\b/gi; 
   }
   $add = join("",$files =~ /[A-Z]\w+/g);
   $add =~ tr/_/ /;
   printf "log((%d+1)/%6d) = %8.4f %s\n",$word_count,$total_words,log(($word_count+1)/$total_words), $add;
}
