#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au August 2015
# as a starting point for COMP2041/9041 assignment 
# http://cgi.cse.unsw.edu.au/~cs2041/assignment/shpy

#Edited by Ryan Shivashankar on the 7th September 2015

my (@imports,@python,@comments);
my $count = 0;

my $for_loop = 0;
my $while_loop = 0;
my $if_else = 0;
my $single_q = 0;
my $iterator = 0;
my $collection = 0;
my $args = 0;
my $glob = 0;
my $sys = 0;
my $os = 0;
my $os_path = 0;

#echo sub variables
my $echo_print = 0; #print_calls variable 
my $pcount = 0;
my $double_q = 0;

#for sub variables
#my $for_print = 0;

#while sub variables
#my $while_print = 0;

#indent count varible
my $my_indentCount = 0;

while ($line = <>) {
   chomp $line;
   imports();
   indent_count();
   if ($line =~ /^#!/ && $. == 1) {
      $print_imports = "#!/usr/bin/python2.7 -u\n";
      push(@imports,$print_imports);

   } elsif ($line =~ /\becho\b /) {
      echo();     

   } elsif ($line =~ /\bfor/ || $line =~ /\bdo/ || $line =~ /\bdone/){
      for_loop();

   } elsif ($line =~ /\bwhile\b/){
      while_loop();

   } elsif ($line =~ /\bif\b/ || $line =~ /\belif\b/ || $line =~ /\belse\b/ || $line =~ /\bthen\b/ || $line =~ /\bfi\b/){
      if_else();

   } elsif ($line =~ /=/) {
      variables();  

   } elsif ($line =~ /\bcd\b/){
      $line =~ s/cd //;
      my @fields = split /cd/,$line;
      $print = "os.chdir('@fields')\n" if $my_indentCount == 1;
      $print = "    os.chdir('@fields')\n" if $my_indentCount == 2;
      $print = "        os.chdir('@fields')\n" if $my_indentCount == 3;
      push(@python,$print);

   } elsif ($line =~ /\bexit\b/) {
      $line =~ /exit (\d)/;
      $print = "    sys.exit($1)\n" if $my_indentCount == 1;
      $print = "        sys.exit($1)\n" if $my_indentCount == 2;
      $print = "            sys.exit($1)\n" if $my_indentCount == 3;
      push(@python,$print);

   } elsif ($line =~ /\bread\b/) {
      $line =~ /\s*(\w+) \s*(\w+)/;
      $collection = $2;
      $line =~ s/\s+\bread\s+//g;
      
      $print = "$collection = sys.stdin.read$collection().rstrip()\n" if $my_indentCount == 1;
      
      push(@python,$print);         

   } else {

      if(!$line){ #if empty line jump to next line
         #next;
         $print = "\n";      
         push(@python,$print);
      } elsif ($line =~ /^#/){
         # Lines we can't translate are turned into comments  
         $print = "$line\n";
         push(@comments,$print);

      } else { 
         #subprocess calls come here  
         $count = 1;
         my $str = $line;
         chomp $str;
         $line=~ s/ /', '/g;
         subprocess();     
      }

   }
}
#my print arrays
print @imports;  #prints imports
print @comments; #prints all lines that are comments
print @python;   #prints the python output

#variable counters in imports sub is to make sure that imports are printed only once per file
sub imports {

   if(($line =~ /\bpwd\b/ || $line =~ /\bls\b/ || $line =~ /\brm\b/) && $count == 0){
      $print_imports = "import subprocess\n";
      push(@imports,$print_imports);
      $count = 1;   
   }

   if(($line =~ /\bexit\b/ || $line =~ /\bread\b/ || $line =~ /\bargument\b/ || $line =~ '\$\@' || $line =~ /\=\$/) && $sys == 0){
      $sys = 1;
      $print_imports = "import sys\n";
      push(@imports,$print_imports);
   }

   if ( ($line =~ /\bcd\b/ || $line =~ /-r\b/) && $os == 0){
      $os = 1;
      $print_imports = "import os\n";
      push(@imports,$print_imports);
   }

   if ($line =~ /\.c/ && $glob == 0){
      $glob = 1;
      $print_imports = "import glob\n";
      push(@imports,$print_imports);
   }

   if ($line =~ /-d\b/ && $os_path == 0){
      $os_path = 1;
      $print_imports = "import os.path\n";
      push(@imports,$print_imports);
   }   
}

#split into two big if statements
#1st if statement handles all those lines having a $
#2nd is for all other cases
sub echo {
      
   $line =~ s/\s+echo //g || $line =~ s/echo //;
   
   if($line =~ /\$/ ){

      if($line =~ /\bargument\b/){
         $line =~ s/ /', '/g;
         $line =~ s/'\$/sys.argv[/g;
         $line =~ s/$/]/g;
         $args = 1;         

      } else {

         if($for_loop == 1){

            if($line =~ /\s*(\$\w+)\s* \s*(\$\w+)\s*/){
               $line =~ /(\w+) \s*(\$\w+)\s* \s*(\$\w+)\s*/g;
               $iterator = $1;
               $collection = join(" ",$2,$3);
               $iterator =~ s/^/'/g;
               $iterator =~ s/$/'/g;               
               $collection =~ s/\$//g;
               $line = join(" ",$iterator,$collection);
               $line =~ s/ /, /g;

            } else {   
               $line =~ s/^/'/g;
               $line =~ s/ /','/g;
               $line =~ s/'\$/ /g;
               $line =~ s/\s*//g;
            }

         } else {

            if($line =~ />>\$/){
               $line =~ s/\$//g;
               $line =~ /(\w+) >>(\w+)/;
               $line ="with open($2, 'a') as f: print >>f, $1";
               $pcount = 1; 

            } else {
               $line =~ s/\$//g;
               $line =~ s/ /, /g;
            }   

         }
      }
          
      #print statements
      $echo_print = 1; 
      print_calls();
      
   } else {
   
      if($line =~ /'/ && $line=~ /'$/){
         $line =~ s/'//g;

      } elsif ($line =~ /"/ && $line=~ /"$/){
         $double_q = 1;

      } else {   
         $line=~ s/ /', '/g;
      }
                  
      #print statements
      print_calls();   

   }   
}

#3 big if statemnts used
#1st handles those that have =$[0-9]
#2nd handles those that have =$[A-Za-z]
#3rd handles those that havve =[0-9]
sub variables {

   if($line =~ /\=\$[0-9]/){
      $line =~ s/=/ = /;
      $line =~ s/\$/sys.argv[/;
      $line =~ s/$/]/;

   } elsif ($line =~ /\$[A-Z]/i){

      if ($line =~ /\=\`/){      
         $line =~ s/`//g;
         $line =~ s/expr//;

         if($line =~ /number/){
            $line =~ s/\'\*\'/* /;
            $line =~ s/\$/\$int(/;
            $line =~ s/\s+\+/) +/;
            $line =~ s/\s+\//) \//;
            $line =~ s/\s+\%/) \%/;

         } else {
            $line =~ s/\$//;
         }  

      } elsif ($line =~ /\=\$\(/){
         $line =~ s/[()]//g;
         $line =~ s/\$/\$int(/;
         $line =~ s/\s+\+/) +/;
      }

      $line =~ s/\s\$/ /g;
      $line =~ s/\$//g;
      $line =~ s/=/ = /;

   } else {

      if($line =~ /=[0-9]/){ 
         $line =~ s/=/ = /;

      } else {
         $line =~ s/=/ /;
         $line =~ s/ / = '/;
         $line =~ s/$/'\$/;
         $line =~ s/\$//;
      }

   }
   print "$line\n";
   $print = "$line\n" if $my_indentCount == 1;
   $print = "    $line\n" if $my_indentCount == 2;
   $print = "        $line\n" if $my_indentCount == 3;
   push(@python,$print);   
}

sub for_loop {

   if(!$while_loop){ #this is to make sure that im in a for_loop
      $for_loop = 1;
   }

   if($line =~ /do/ || $line =~ /done/){ #Get rid of do and done  
      $line =~ s/do//g;    

      if($line =~ /done/){ #for loop ends here
         $for_loop = 0; 
      }

      $line =~ s/done//g;

   } elsif ($line =~ /\.c/) {
      $line =~ s/\*\.c/sorted(glob.glob("*.c"))/g;
      my @forloop = split / /,$line;      
      $print = "@forloop:\n" if $my_indentCount == 1;
      $print = "    @forloop:\n" if $my_indentCount == 2;
      $print = "        @forloop:\n" if $my_indentCount == 3;
      push(@python,$print);

   } else {
      $line =~ /for \s*([a-zA-Z_]\w*)\s* in \s*(.*)/;
      $iterator = $1;
      $collection = $2;     

      if($collection =~ /[a-zA-Z]/){
         $collection =~ s/^/'/g;
         $collection =~ s/$/'/;
         $collection =~ s/ /', '/g;
         $collection =~ s/\'(\d+)\'/$1/g;
      }

      my @forloop = split / /,$collection;      
      $print = "for $iterator in @forloop:\n" if $my_indentCount == 1;
      $print = "    for $iterator in @forloop:\n" if $my_indentCount == 2;
      $print = "        for $iterator in @forloop:\n" if $my_indentCount == 3;
      push(@python,$print);
   }
}

sub while_loop {
   $while_loop = 1;   
   
   if($line =~ /true/){
      $line =~ s/true/not subprocess.call(['true'])/;
   
   } else {
      #change characters into their equivalent signs     
      if($line =~ /-gt/ || $line =~ /-o/ || $line =~ /-lt/ || $line =~ /-eq/){
         $line =~ s/-gt/>/;
         $line =~ s/-o/or/;
         $line =~ s/-lt/</;
         $line =~ s/-eq/==/;
      }
      
      if($line =~ /</){
         $line =~ s/\s</) </;
      }
         
      $line =~ s/test\s+//;
      $line =~ s/\$/int(/g;
      $line =~ s/\s+-le/) <=/;
      $line =~ s/$/)/;
      
      if($line =~ /[\[\]]/){
         $line =~ s/\s+[\[\]]//g;
         if ($line =~ /\d\)/){
            $line =~ s/\)$//;
         }
      }

   }   

   my @whileloop = split / /,$line;         
   $print = "@whileloop:\n" if $my_indentCount == 1;
   $print = "    @whileloop:\n" if $my_indentCount == 2;
   $print = "        @whileloop:\n" if $my_indentCount == 3;
   push(@python,$print);

}

#3 sepertate if statemnts 
#1st is for all those on the if or elif lines <- this is the biggest
#2nd is to get rid of the then and fi
#3rd makes the else into else:
sub if_else {
   $if_else = 1; 

   if($line =~ /if/ || $line =~ /elif/){
      $line =~ s/test//;
      $line =~ s/\s+/ /g;
      
      if($line =~ /\$\#/) {
         $line =~ s/\$\#/len(sys.argv[1:])/g;
         
         if($line =~ /-gt/){ #handle level 4 case 
            $line =~ s/$/:/;
         }
         
      }
      
      #change letters into their respective signs   
      if($line =~ /-gt/ || $line =~ /-o/ || $line =~ /-lt/ || $line =~ /-eq/){         
         $line =~ s/-gt/>/;
         $line =~ s/-o/or/;
         $line =~ s/-lt/</;
         $line =~ s/-eq/==/;
         
         if($line =~ /$/){
            
            if($line !~ /==/){
            
               if ($line =~ /\[ \$/){
                  $line =~ s/$/:/;
               }
               
               $line =~ s/\$/int(/g;
               $line =~ s/ >/) >/g;
               $line =~ s/ </) </g;
            
            } else {
               $line =~ s/\$//g;
            }
            
         }
         
      } elsif($line =~ /-r/){  # -r flag        
         $line =~ s/-r/os.access('/g;
         
         if($line =~ /\$/){
            $line =~ s/'\s+\$//;
            $line =~ s/$/, os.R_OK):/g;
         
         } else {
            $line =~ s/'\s+/'/g;
            $line =~ s/$/', os.R_OK):/g;
         }
         
      } elsif($line =~ /-d/){ # -d flag
         $line =~ s/-d/os.path.isdir('/g;
         $line =~ s/'\s+/'/g;
         $line =~ s/$/'):/g; 
         
         if($line =~ /[\[\]]/){
            $line =~ s/\s+[\[\]]//g;
            $line =~ s/\s+\'\)\:/'):/g;      
         }
          
      } elsif($line =~ /fgrep/){      
         $line =~ /if (\s*\w+) (-\w) (-\w) (\$\w+) (\$\w+)/;
         $iterator = join(" ",$1,$2,$3);
         $collection = join (" ",$4,$5);
         $iterator =~ s/^/'/;
         $iterator =~ s/ /','/g;
         $iterator =~ s/$/',/;
         $collection =~ s/\$/str(/g;
         $collection =~ s/ /), /g;
         $collection =~ s/$/)/;
         $data = join(" ",$iterator,$collection);
         $line = "   if not subprocess.call([$data]):";
         
      } else {

         if ($line =~ /\$/) {
            $line =~ s/\$//g;
            $line =~ s/$/:/;
         } else {         
            $line =~ s/ /'/g;
            $line =~ s/if'/if '/g;
            $line =~ s/!=/ != /;     
            $line =~ s/=/ == /g;
            $line =~ s/$/':/g;         
         }
      }
      
      my @if_else = split / /,$line;
      $print = "@if_else\n" if $my_indentCount == 1;
      $print = "    @if_else\n" if $my_indentCount == 2;
      $print = "        @if_else\n" if $my_indentCount == 3;
      push(@python,$print);
            
   }
   
   if($line =~ /then/ || $line =~ /fi/){         
      $line =~ s/then//g;
      
      if($line =~ /fi/){ #if statement ends here
         $if_else = 0;
      }
      
      $line =~ s/fi//g;
   }
   
   if($line =~ /else/){
      $line =~ s/else/else:\n/ if $my_indentCount == 1;
      $line =~ s/else/    else:\n/ if $my_indentCount == 2;
      $line =~ s/else/        else:\n/ if $my_indentCount == 3;
      push(@python,$line);
   }
   
}

sub subprocess {
   
   if($line =~ '\$\@'){
      $line =~ s/\$\@/sys.argv[1:]/g;
      $line =~ s/, '"s/] + s/g;
      $line =~ s/]"/]/g;
      $line =~ s/l/['l/;
      my @fields = split / /,$line;
      $print = "subprocess.call(@fields)\n" if $my_indentCount == 1;
      $print = "    subprocess.call(@fields)\n" if $my_indentCount == 2;
      $print = "        subprocess.call(@fields)\n" if $my_indentCount == 3;
      push(@python,$print);
   
   } elsif ($line =~ /rm/) {
      $line =~ s/^/'/;      
      $line =~ s/'\$/str(/;
      $line =~ s/$/)/;
      my @fields = split / /,$line;
      $print = "subprocess.call([@fields])\n" if $my_indentCount == 1;
      $print = "    subprocess.call([@fields])\n" if $my_indentCount == 2;
      $print = "        subprocess.call([@fields])\n" if $my_indentCount == 3;
      push(@python,$print);
   
   } else {
      my @fields = split / /,$line;
      $print = "subprocess.call(['@fields'])\n" if $my_indentCount == 1;
      $print = "    subprocess.call(['@fields'])\n" if $my_indentCount == 2;
      $print = "        subprocess.call(['@fields'])\n" if $my_indentCount == 3;
      push(@python,$print);
   }
   
}

sub indent_count {
   
   if($line =~ /\bif\b/ || $line =~ /\bwhile\b/ || $line =~ /\bfor\b/){
      $my_indentCount++;
      print "$my_indentCount\n";
   }
   
   if($line =~ /\bfi\b/ || $line =~ /\bdone\b/){
      $my_indentCount--;
      print "$my_indentCount\n";
   }
}

sub print_calls {
   if($echo_print == 1){
      my @ech = split /echo /,$line;
      
      if ($for_loop == 1){
         #print statments like these are to get them indented into python way
         $print = "    print @ech\n" if $my_indentCount == 1;
         $print = "        print @ech\n" if $my_indentCount == 2;
         $print = "            print @ech\n" if $my_indentCount == 3;
         push(@python,$print);
         $for_loop = 0;   

      } elsif ($args == 1){
         $print = "print '@ech\n" if $my_indentCount == 1;
         $print = "    print '@ech\n" if $my_indentCount == 2;
         $print = "        print '@ech\n" if $my_indentCount == 3;
         push(@python,$print);      

      } elsif ($pcount == 1){
         $print = "    @ech\n" if $my_indentCount == 1;
         $print = "        @ech\n" if $my_indentCount == 2;
         $print = "            @ech\n" if $my_indentCount == 3;
         push(@python,$print);

      } elsif ($while_loop == 1){
         $print = "    print @ech\n" if $my_indentCount == 1;
         $print = "        print @ech\n" if $my_indentCount == 2;
         $print = "            print @ech\n" if $my_indentCount == 3;
         push(@python,$print);   

      } else {
         $print = "print @ech\n" if $my_indentCount == 1;
         $print = "    print @ech\n" if $my_indentCount == 2;
         $print = "        print @ech\n" if $my_indentCount == 3;
         push(@python,$print);
      }
   } else {
      my @ech = split /echo /,$line;
      if ($for_loop == 1){
         $print = "    print '@ech'\n" if $my_indentCount == 1;
         $print = "        print '@ech'\n" if $my_indentCount == 2;
         $print = "            print '@ech'\n" if $my_indentCount == 3;
         push(@python,$print);
         $for_loop = 0;

      } elsif ($if_else == 1){
         $print = "    print '@ech'\n" if $my_indentCount == 1;
         $print = "        print '@ech'\n" if $my_indentCount == 2;
         $print = "            print '@ech'\n" if $my_indentCount == 3;
         push(@python,$print);      

      } else {

         if($double_q == 1){
            $print = "print @ech\n" if $my_indentCount == 1;
            $print = "    print @ech\n" if $my_indentCount == 2;
            $print = "        print @ech\n" if $my_indentCount == 3;

         } else {      
            $print = "print '@ech'\n" if $my_indentCount == 1;
            $print = "    print '@ech'\n" if $my_indentCount == 2;
            $print = "        print '@ech'\n" if $my_indentCount == 3;
         }

         push(@python,$print);
      }
   }
   
      
}
   
