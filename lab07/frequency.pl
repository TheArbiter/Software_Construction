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
   printf "%4d/%6d = %.9f %s\n",$word_count,$total_words,$word_count/$total_words, $add;
}
