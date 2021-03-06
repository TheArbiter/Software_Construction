#!/usr/bin/perl -w

$r_flag = 1;
$count = 0;
$i = 0;

die if @ARGV == 0;
if ($#ARGV == 1){
   $r = 1;
   shift @ARGV;
}

$url_under = "http://www.handbook.unsw.edu.au/undergraduate/courses/2015/$ARGV[0].html";
$url_post = "http://www.handbook.unsw.edu.au/postgraduate/courses/2015/$ARGV[0].html";
  
sub files{   
   unless (open F, "wget -q -O- $url_under|"){
      $f1 = 0;
   }
   unless (open G, "wget -q -O- $url_post|"){
      $f2 = 0;
   }
   
   if(!$f1){
      while ($line = <F>) {
         if($line =~ m/>P(rerequisite.*?)</ || $line =~ m/>pre-r(equisite.*?)</ || $line =~ m/>Pre-R(equisite.*?)</ || $line =~ m/>P(re.*?)</){
            @temp = ($1 =~ m/([A-Za-z]{4}\d{4})/g);
            tr/a-z/A-Z/ foreach (@temp);
            push(@prereq_u, @temp);
         }  
      }
   }    
   @temp = ();
   
   if (!$f2){
      while ($line = <G>) {
         if($line =~ m/>P(rerequisite.*?)</ || $line =~ m/>pre-r(equisite.*?)</ || $line =~ m/>Pre-R(equisite.*?)</ || $line =~ m/>P(re.*?)</){
            @temp = ($1 =~ m/([A-Za-z]{4}\d{4})/g);
            tr/a-z/A-Z/ foreach (@temp);
            push(@prereq_p, @temp);
         }
      }
   }   
}

files();

if (@prereq_u == -1 and @prereq_p == -1){
   $r_flag = 0;
} else {
   push(@prereq, @prereq_u);
   push(@prereq, @prereq_p);
}   

if ($r){
   while($r_flag){
      $count = 1 + $#prereq_u + $#prereq_p;
      @prereq_u = ();
      @prereq_p = ();
      $course = $prereq[$i];
      $temp = $i;
      
      while($i <= $temp + $count){
         $url_under = "http://www.handbook.unsw.edu.au/undergraduate/courses/2015/$course.html";
         $url_post = "http://www.handbook.unsw.edu.au/postgraduate/courses/2015/$course.html";
           
         files();
       
         $i = $i + 1;
         $course = $prereq[$i];
      }
      if ($#prereq_u == -1 and $#prereq_p == -1){
         $r_flag = 0;
      } else {
         push(@prereq, @prereq_u);
         push(@prereq, @prereq_p);
      }              
   }   
}

sub u {
   my %data;
   grep !$data{$_}++,@_;
}
@prereq = u(@prereq);
@prereq = sort @prereq;
   
print join("\n",@prereq);
print "\n";
