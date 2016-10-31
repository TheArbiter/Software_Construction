#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2015
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/bitter/

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;

sub main() {
if(param("username") ne ""){
	  	$c = CGI::Cookie->new(-name =>"username",
                         -value   =>{username => param("username"),param("password")},
                    );
}
	#Set-Cookie: sessionToken=abc123; Expires=Wed, 09 Jun 2021 10:18:14 GMT
    # print start of HTML ASAP to assist debugging if there is an error in the script
	
	print page_header();
    # Now tell CGI::Carp to embed any warning in HTML
    warningsToBrowser(1);
    
    # define some global variables
    $debug = 1;
	$count = 0;
    $dataset_size = "medium"; 
    $users_dir = "dataset-$dataset_size/users";
	$bleats_dir = "dataset-$dataset_size/bleats";
	$bootstrap_files ="bootstrap-3.3.5/docs/examples";
	$user_to_show = 0;
	$thereIsReply = 0;
	$authenicated = 0;
	$change = 0;
	$n = 0;
	$Greenlight = 0;
	$passWho = 0;
	$ShowText = 0;
	homepage();
    print page_trailer();
}

#
# HTML placed at the top of every page
#
sub page_header {
print header (-cookie=>$c);
   return <<eof


<!DOCTYPE html>
<html lang="en">
<head>
<title>Bitter</title>
<link href="bitter.css" rel="stylesheet">
    <link rel="icon" href="../../favicon.ico">
    <!-- Bootstrap core CSS -->
    <link href="bootstrap-3.3.5/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
eof
}

#
# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}


sub login_page {

	#print "username: ";
	$username = param("username");
	#print "password: ";
	$password = param("password");
	
	# sanitize username
	$username = substr $username, 0, 256;
	$username =~ s/\W//g;
	$loggedin_User = param("username");
	$loggedin_User=~ s/\W//g;

	# This part is when they reach the search bar it will check who was typed as the username
	# And then it will check if the intial password that was used to authenticate is still the same
	# If so then it will show the user who was requested in the search bar
	if ($loggedin_user && $loggedin_pass){
		$user_to_show = "$users_dir/$loggedin_user";
		user_page();
	} elsif ($username && ($passWho eq $password)){
			$user_to_show = "$users_dir/$username";
			user_page();		
	} else {
		# This is the intial part that is used to log in
		if ($username && $password){
			#Check database with given Username and password to see if they exist
			#if the exist open them
			open $user, "<$users_dir/$username";
			$password_file = "$users_dir/$username/password";
			open F, "<$password_file";
			$correct_password = <F>;	
			chomp $correct_password;
			$pass = $password eq $correct_password;	
		
			if (!$user) {
				 print "Unknown username!\n";
			} else {
				 if ($pass) {
					$count = 1;
					$user_to_show = "$users_dir/$username";
					user_page();
				 } else {
					cover_page();
					print "Incorrect username or password!\n"; #Doesn't go through the if !user
				 }
			}	
		} else {
			cover_page();
		}
	}
	
}
sub signup {

	$newUsername = param("newusername");
	$newPassword = param("newpassword");
	$firstName = param("firstname");
	$lastName = param("lastname");
	$email_addr = param("email");

	# sanitize username
	$newUsername = substr $newUsername, 0, 256;
	$newUsername =~ s/\W//g;

	# sanitize password
	$newPassword = substr $newPassword, 0, 256;
	$newPassword =~ s/\W//g;

	# sanitize firstName
	$firstName = substr $firstName, 0, 256;
	$firstName =~ s/\W//g;

	# sanitize lastName
	$lastName = substr $lastName, 0, 256;
	$lastName =~ s/\W//g;
	
	@users = sort(glob("$users_dir/*"));
	while(scalar(@users) !=0){
		$temp = pop @users;
		$temp =~ s/dataset-medium\/users\///g;
		if($temp eq param("newusername")){
			print "Username Already Exist\n";
		} else {
			$Greenlight = 1;
		}
	}
	if($Greenlight != 0){
		#make new directory for the user
		my $directory = "$users_dir/$newUsername";
	
		#check if the directory was made
		unless(mkdir $directory){
			$buffer = "Unable to create $directory\n";
		}

		$fullName = "full_name: $firstName $lastName\n";
		$newUsername = "username: $newUsername\n";
		$passwordFile = "$newPassword\n";
		$newPassword = "password: $newPassword\n";
		$email_addr = "email: $email_addr\n";
	
		#create details.txt
		open my $create_details_file, ">","$directory/details.txt" or die "Can't open $directory/details.txt : $! \n";
		chomp $create_details_file;
		print $create_details_file "$fullName";
		print $create_details_file "$email_addr";
		print $create_details_file "$newUsername";
		print $create_details_file "$newPassword";
		close $create_details_file;

		#create password file
		open my $create_new_password_file, ">", "$directory/password" or die "Can't open $directory/password: $!";
		chomp $create_new_password_file;
		print $create_new_password_file "$passwordFile";
		close $create_new_password_file;

		#create new bleat file
		open my $create_new_bleat_file, ">>", "$directory/bleats.txt" or die "Can't open $directory/bleats.txt: $!";
		chomp $create_new_bleat_file;
		close $create_new_bleat_file;
		login_page();
	} else {
		login_page();
		print "Username Already Exist\n";
	}
}
sub homepage {
	if(defined(param("newusername"))){
		signup();		
	}else {
		login_page();
	}
}

sub search_bar {

	$ifFullName = s/\W//g;
	@users = sort(glob("$users_dir/*"));
	while(scalar(@users) !=0){
		$temp = pop @users;
		open $F,"<","$temp/details.txt" or die "can not open $temp: $!";
		$check = join "\n",<$F>;
		if($check=~ /full_name: (\w*\s\w*)/ || $check=~ /full_name: (\w*-\w*\s\w*)/){
			$checkFN = $1; #Full Name
			$checkFN =~ s/\W//g;
		}
		if($ifFullName eq $checkFN){
			if($check=~ /username: (\w*)\s/){
				$checkUN = $1;
				$change = 1;
				$username = $1;
			}
		} else {
			$checkUN = $ifFullName;
		}
		close $F;
	}
}

#
# Show unformatted details for user "n".
# Increment parameter n and store it as a hidden variable
#
sub user_page {
	#GET ME THEM COOKIES
	%cookies = CGI::Cookie->fetch;
	#$coks = "!=*$cookies{username}*=!\n";
	$cookies{username}=~ m/.*&username&(.*)/;$loggedin_user = $1;
	$loggedin_user =~ s/;.*//;
	$cookies{username}=~ m/.*username=(.*)&&/;$loggedin_pass = $1;
	#GOT THEM COOKIES

	$n = 0;
	$i = 0;
	#static_nav_bar();
	#print display_navbar();
	#cover_pics();

	#Init values
	$catch_name = 0;
	$catch_u_name = 0;
	$catch = 0;
	$catchlat = 0;
 	$catchlong = 0;
    #my $n = param('n') || 0;
    #my @users = sort(glob("$users_dir/*"));
    #my $user_to_show  = $users[$n % @users];

###					###
	###Search Bar###
###					###
	if(defined(param("username")) && $authenicated != 0){
			$ifFullName = param("username");
		#if($ifFullName=~ /(\w*\s\w*)/){
			search_bar();
		#}	
		login_page();
	}
	$authenicated = 1;

###						###
	###END Search Bar###
###						###

	my $details_filename = "$user_to_show/details.txt";

	#Profile Pic 	
	$image_path = "$user_to_show/profile.jpg";
	if (-e "$image_path"){	
		$buffer = "Exist\n";
	} else {
		$image_path="empty_profile.jpg";
	}
	#Cover Pic
	$Cover_path = "$user_to_show/cover.jpg";
	if(-e "$Cover_path"){
		$buffer = "Exist\n";
	} else {
		$Cover_path = "cover.jpg"
	}

	#User Details
	open my $p, "$details_filename" or die "can not open $details_filename: $!";    
	$details = join " ", <$p>;	

	#Removes password from details list and also create a new password file
	if($details=~ /(password: \w+)\s/){
		
		#Creates Password file
		$catch =~ /(password: \w+)\s/;
		my $check_password = $1;
		$check_password =~ s/password: //;	
		open my $create_password_file, ">","$user_to_show/password" or die "Can't open $user_to_show/password : $! \n";
		print $create_password_file "$check_password";
		close $create_password_file;
		
		#Removes Password from bitter profile page	
		$details=~ s/(password: \w+)\s//;
	}

	#Removes email address from details list (for most of them at least need a new method for this)
	if($details=~ /(email: .*)\s/){
		$details=~ s/(email: .*)//;
	}

	#Removes Name and puts it ontop 
	if($details=~ /full_name: (\w*\s\w*)/ ||$details=~ /full_name: (\w*-\w*\s\w*)/){
		$catch_name =~ /full_name: (\w*\s*\w*)\s/;
		$full_name = $1;
		$full_name =~ s/full_name: //;
		$details=~ s/(full_name: \w*\s*\w*)\s//;
	}

	#Removes Username and puts it bellow fullname and adds an @ sign like in twitter 
	if($details=~ /(username: \w*)/){
		$catch_u_name =~ /(username: \w*)\s/;
		$user_name = $1;
		$user_name =~ s/username: /@/;
		$currUser = "$user_name";
		$currUser =~ s/@//;
		$details=~ s/(username: \w*\s*\w*)\s//;
	}
	
	#Get home_longitude and latitude
	if($details=~/(home_longitude: \d*.\d*)/){
		$catchlong =~ /(home_longitude: \d*.\d*)\s/;
		$catchlong = $1;
		$details =~ s/(home_longitude: \d*.\d*)\s//;
	}
	if($details=~ /(home_latitude: -\d*.\d*)/){
		$catchlat =~ /(home_latitude: \d*.\d*)\s/;
		$catchlat = $1;
		$details =~ s/(home_latitude: -\d*.\d*)//;
	}
    close $p;

###					###
	###FOLLOWING###
###					###

	open my $f, "<","$user_to_show/details.txt" or die "can not open $users: $!";
	$following = join "\n", <$f>;
	if($following=~ /listens: (.*)/){
		$catchListens = $1;
		@listens = split / /, $catchListens;
		@HomeShow = @listens; #This is used to display the home bleats
	}
	close $f;
	while(scalar(@listens) !=0){
		$userListens = pop @listens;
		open my $l, "<","$users_dir/$userListens/details.txt" or die "can not open $users_dir/$userListens/details.txt: $!";
		$lis = join "\n",<$l>;
		if($lis =~ /username: (\w*)/){
			$followingIs = $1;
		}
		if($lis=~ /full_name: (\w*\s\w*)/ ||$lis=~ /full_name: (\w*-\w*\s\w*)/){
			$followingName = $1;
		}
		$followingImage_path = "$users_dir/$userListens/profile.jpg";
		if(-e "$followingImage_path"){
			$buffer = "Exist\n";
		} else {
			$followingImage_path ="empty_profile.jpg";
		}
		$disfo = display_following();
		push(@displayfollowing,$disfo);
	}
	close $l;	
	

###						###
	###END FOLLOWING###
###						###


###					###
	###FOLLOWERS###
###					###
	my @users = sort(glob("$users_dir/*"));	
	while(scalar(@users) !=0){
		$users = pop @users;
		open my $userList, "<","$users/details.txt" or die "can not open $users: $!";
		$det = join "\n",<$userList>;
		if ($det=~ /(listens: .*)/){
			$det=~ /(listens: .*):/;
			$userLis = $1;
			#Check if User is in the follower listens
			if($userLis=~ /.*($currUser).*/){
				if($det=~ /username: (\w*)/){
					$followerIs = $1;
				}
				if($det=~ /full_name: (\w*\s\w*)/ ||$det=~ /full_name: (\w*-\w*\s\w*)/){
					$followerName = $1;
				}
				$followerImage_path = "$users/profile.jpg";
				if (-e "$followerImage_path"){	
					$buffer = "Exist\n";
				} else {
					$followerImage_path="empty_profile.jpg";
				}
				$dis = display_followers();
				push(@displayfollowers,$dis);
			}	
		}
		close $userList;
	}

###						###
	###END FOLLOWERS###
###						###


###				###
	###Bleats###	
###				###
	open my $bl, "<","$user_to_show/bleats.txt" or die "can not open $user_to_show/bleats.txt: $!";
	chomp (@tweetIds = (<$bl>));
	close $bl;
	while(scalar(@tweetIds) !=0){
		$tweetLoc = pop @tweetIds;
		$TweetI = "$tweetLoc";
		#Get the bleat to display on profile page
		open my $tweet, "<","$bleats_dir/$tweetLoc" or die "can not open $bleats_dir/$tweetLoc: $!";	
		$bleats = join '', <$tweet>;
		#Removes Username from bleats
		if($bleats=~ /(username: \w+)\s/){
			$bleats=~ s/(username: \w+)\s//;
		}
		#Removes latitude
		if($bleats=~ /(latitude: -\d+.\d+)\s/){
			$bleats=~ s/(latitude: -\d+.\d+)\s//;
		}
		#Removes longitude
		if($bleats=~ /(longitude: \d+.\d+)\s/){
			$bleats=~ s/(longitude: \d+.\d+)\s//;
		}
		#Removes time
		if($bleats=~ /(time: \d+)\s/){
			$bleats=~ s/(time: \d+)\s//;
		}
		#Removes Fullname from bleats
		if($bleats=~ /full_name: (\w*-\w*\s\w*)/ || $bleats=~ /full_name: (\w*\s\w*)/){
			$bleats=~ s/(full_name: \w*-\w*\s\w*)//;
			$bleats=~ s/(full_name: \w*\s\w*)//;
		}
		#Removes in_reply_to
		if($bleats=~ /(in_reply_to: \d+)\s/){
			$bleats=~/in_reply_to: (\d+)\s/;
			$inReply = $1;
			$bleats=~ s/(in_reply_to: \d+)\s//;
			bleat_reply();
		}
		if($thereIsReply != 0){
			bleat_reply();
		}
		$showBleat = display_bleats();
		push(@bleatsFile,$showBleat);	
		close $tweet;
	}
###					###
	###END BLEATS###
###					###
	#Profile Text
	if(defined(param("ProfileText"))){
		profile_text();
	}
	if(-e "$user_to_show/profiletext.txt"){	
		open $Y, "<","$user_to_show/profiletext.txt" or die "Can not open $user_to_show/profiletext.txt :$!";
		$ShowText = join "\n",<$Y>;
		close $Y;
	}

	#if(defined(param("Listening"))){
	#	remove_following();
	#}

	if(defined(param("DeleteTweet"))){
		delete_bleat();
	}

	home_bleats();
	$current_user_page = current_user_page();
	push(@current_user_page,$current_user_page);

    #Edit profile details
    if(defined(param("FirstName"))){
		edit_user_profile();
	}
	$edit_pro = edit_profile();
	push(@edit_Profile,$edit_pro);

	if(defined(param("Confirm Email"))){
		delete_user_account();
		if($cantpass == 0){
			print confirm_delete();
		}
	}
	$deleteA = delete_account();
	push(@del_account,$deleteA);
	print user_home_page();
	
}

sub home_bleats {
###					###
	###HOME BLEATS###
###					###

	#New Bleats
	if(defined(param("newbleat"))){
		create_bleat();
	}

	#Get all tweet Id's
	while(scalar(@HomeShow) !=0){
		$HomeUser = pop @HomeShow;
		#Open that users directory and take their bleats.txt and push it into an array
		open $y, "<","$users_dir/$HomeUser/bleats.txt" or die "Can't open $users_dir/$HomeUser/bleats.txt";
		chomp(@homeTweetId = (<$y>));
		push(@homeTwId,@homeTweetId);
		close $y;
	}
		#Sort all the Id's
		@sortedIds = sort (@homeTwId);
	
	#Pop the array and open each individiual Id
	while(scalar(@sortedIds) !=0){
		$TweetUsrId = pop @sortedIds;
		open $z, "<","$bleats_dir/$TweetUsrId" or die "Can't open $bleats_dir/$TweetUsrId";
		$HomeBleats = join "\n",<$z>;
		
		#Get and Removes Username from bleats
		if($HomeBleats=~ /username: (\w+)\s/){
			$GetUname = $1;
			$HomeBleats=~ s/(username: \w+)\s//;
		}
		#Removes latitude
		if($HomeBleats=~ /(latitude: -\d+.\d+)\s/){
			$HomeBleats=~ s/(latitude: -\d+.\d+)\s//;
		}
		#Removes longitude
		if($HomeBleats=~ /(longitude: \d+.\d+)\s/){
			$HomeBleats=~ s/(longitude: \d+.\d+)\s//;
		}
		#Removes time
		if($HomeBleats=~ /(time: \d+)\s/){
			$HomeBleats=~ s/(time: \d+)\s//;
		}
		#Removes in_reply_to
		if($HomeBleats=~ /(in_reply_to: \d+)\s/){
			$HomeBleats=~/in_reply_to: (\d+)\s/;
			$HomeBleats=~ s/in_reply_to: (\d+)\s//;
		}
		#Removes Fullname
		if($HomeBleats=~ /full_name: (\w*-\w*\s\w*)/ || $HomeBleats=~ /full_name: (\w*\s\w*)/){
			$HomeBleats=~ s/(full_name: \w*-\w*\s\w*)//;
			$HomeBleats=~ s/(full_name: \w*\s\w*)//;
		}
		close $z;
		
		#From the Username we got through #GetUname open their user directory
		open $u, "<","$users_dir/$GetUname/details.txt" or die "Can't open $users_dir/$GetUname/details.txt";
		$dets = join "\n",<$u>;	
		#Get their full name
		if($dets=~ /full_name: (\w*\s\w*)/ ||$dets=~ /full_name: (\w*-\w*\s\w*)/){
			$followerHomeName = $1;
		}
		#Get their pro pic 
		$followerHomeImage_path = "$users_dir/$GetUname/profile.jpg";
		if (-e "$followerHomeImage_path"){	
			$buffer = "Exist\n";
		} else {
			$followerHomeImage_path="empty_profile.jpg";
		}
		close $u;
		$showHomeBleat = display_home_bleat();
		push(@HomeBleatsFile,$showHomeBleat);
	}

###						###
   ###HOME END BLEATS###
###						###
	$current_home_page = current_home_page();
	push(@current_home_page,$current_home_page);
}

sub create_bleat {
	$newbleat = param("newbleat");
	$newbleat =~ s/\W/ /g;

	$idCount = 2041954300 +$n;

	#Create tweet file
	$tweetfile = "$bleats_dir/$idCount", $n++;
	
	open  $create_tweet_file, ">","$tweetfile" or die "Can't open $tweetfile : $! \n";
	chomp $create_tweet_file;
	print $create_tweet_file "username: $username\n";
	print $create_tweet_file "bleat: $newbleat\n";
	close $create_tweet_file;
   
    open $input_id_num, ">>","$user_to_show/bleats.txt" or die "can not open $user_to_show/bleats.txt: $!\n";
	print $input_id_num "$idCount\n";
    close $input_id_num;

	#UploadBleatPic Pic #IF THIS EVER WORKS
		if(defined(param("UploadBleatPic"))){
		$Bleat_Img = "$users_dir/$loggedin_User/bleat.jpg";
		$uploadCoverPic = upload('UploadBleatPic');
		open($bp,">",$Bleat_Img) or die;
		binmode $bp;
		while($line = <$uploadCoverPic>){
			$pic = print $bp $line;
		}
		$displayIMG = display_image_bleats();
		push(@displayIM,$displayIMG);
		close $bp;
	}
	
}

sub bleat_reply {
	#Get bleat/s that will be shown in reply to bleat displayed on user page
	open my $bleatReply, "<","$bleats_dir/$inReply" or die "can not open $bleats_dir/$inReply: $!";
	$bleatRep = join "\n", <$bleatReply>;
	#Removes Username from bleats
	if($bleatRep=~ /username: (\w+)\s/){
		$GetBleatUname = $1;
		$bleatRep=~ s/(username: \w+)\s//;
	}

	#From the Username we got through #GetBleatUname open their user directory
	open $v, "<","$users_dir/$GetBleatUname/details.txt" or die "Can't open $users_dir/$GetBleatUname/details.txt";
	$detsb = join "\n",<$v>;	
	#Get their full name
	if($detsb=~ /full_name: (\w*\s\w*)/ ||$detsb=~ /full_name: (\w*-\w*\s\w*)/){
		$followerReplyName = $1;
	}
	close $v;

	#Get their pro pic
	$BleatImage_path = "$users_dir/$GetBleatUname/profile.jpg";
	if (-e "$BleatImage_path"){	
		$buffer = "Exist\n";
	} else {
		$BleatImage_path="empty_profile.jpg";
	}

	#Removes latitude
	if($bleatRep=~ /(latitude: -\d+.\d+)\s/){
		$bleatRep=~ s/(latitude: -\d+.\d+)\s//;
	}
	if($bleatRep=~ /(latitude: \d+.\d+)\s/){
		$bleatRep=~ s/(latitude: \d+.\d+)\s//;
	}
	#Removes longitude
	if($bleatRep=~ /(longitude: \d+.\d+)\s/){
		$bleatRep=~ s/(longitude: \d+.\d+)\s//;
	}
	#Removes time
	if($bleatRep=~ /(time: \d+)\s/){
		$bleatRep=~ s/(time: \d+)\s//;
	}
	#Removes Fullname
	if($bleatRep=~ /full_name: (\w*-\w*\s\w*)/ || $bleatRep=~ /full_name: (\w*\s\w*)/){
			$bleatRep=~ s/(full_name: \w*-\w*\s\w*)//;
			$bleatRep=~ s/(full_name: \w*\s\w*)//;
	}
	#Removes in_reply_to
	if($bleatRep=~ /(in_reply_to: \d+)\s/){
		$bleatRep=~/in_reply_to: (\d+)\s/;
		$inReply = $1;
		$thereIsReply = 1;
		$bleatRep=~ s/(in_reply_to: \d+)\s//;
		$replyUserBleat = display_reply_bleats();
		push(@ReplyUsrBleat,$replyUserBleat);
	}  else {
		$thereIsReply = 0;
		$replyUserBleat = display_reply_bleats();
		push(@ReplyUsArBleat,$replyUserBleat);
	}
	close $bleatReply;
}

sub bleat_home_reply {
	#Get bleat/s that will be shown in reply to bleat displayed on home page
	open my $bleatHomeReply, "<","$bleats_dir/$homeinreply" or die "can not open $bleats_dir/$homeinreply: $!";
	$bleatHRep = join "\n", <$bleatHomeReply>;

	#Removes Username from bleats
	if($bleatHRep=~ /username: (\w+)\s/){
		$GetBleatHUname = $1;
		$bleatHRep=~ s/(username: \w+)\s//;
	}

	#From the Username we got through #GetBleatUname open their user directory
	open $b, "<","$users_dir/$GetBleatHUname/details.txt" or die "Can't open $users_dir/$GetBleatUname/details.txt";
	$detshb = join "\n",<$b>;
	
	#Get their full name
	if($detshb=~ /full_name: (\w*\s\w*)/ ||$detshb=~ /full_name: (\w*-\w*\s\w*)/){
		$followerHomeReplyName = $1;
	}
	close $b;

	$BleatHomeImage_path = "$users_dir/$GetBleatHUname/profile.jpg";
	if (-e "$BleatHomeImage_path"){	
		$buffer = "Exist\n";
	} else {
		$BleatHomeImage_path="empty_profile.jpg";
	}

	#Removes latitude
	if($bleatHRep=~ /(latitude: -\d+.\d+)\s/){
		$bleatHRep=~ s/(latitude: -\d+.\d+)\s//;
	}
	if($bleatHRep=~ /(latitude: \d+.\d+)\s/){
		$bleatHRep=~ s/(latitude: \d+.\d+)\s//;
	}
	#Removes longitude
	if($bleatHRep=~ /(longitude: \d+.\d+)\s/){
		$bleatHRep=~ s/(longitude: \d+.\d+)\s//;
	}
	#Removes time
	if($bleatHRep=~ /(time: \d+)\s/){
		$bleatHRep=~ s/(time: \d+)\s//;
	}
	#Removes Fullname
	if($bleatHRep=~ /full_name: (\w*-\w*\s\w*)/ || $bleatHRep=~ /full_name: (\w*\s\w*)/){
			$bleatHRep=~ s/(full_name: \w*-\w*\s\w*)//;
			$bleatHRep=~ s/(full_name: \w*\s\w*)//;
	}
	#Removes in_reply_to
	if($bleatHRep=~ /(in_reply_to: \d+)\s/){
		$bleatHRep=~/in_reply_to: (\d+)\s/;
		$homeinreply = $1;
		$thereIsReply = 1;
		$bleatHRep=~ s/(in_reply_to: \d+)\s//;
		$replyHomeUserBleat = display_home_reply_bleat();
		push(@ReplyHomeBleat,$replyHomeUserBleat);
	}  else {
		$thereIsReply = 0;
		$replyHomeUserBleat = display_home_reply_bleat();
		push(@ReplyHomereplyBleat,$replyHomeUserBleat);
	}
	close $bleatHomeReply;
}

sub delete_bleat {
	#Delete Bleat from bleats directory
	$BleatsDirecRM = "$bleats_dir/$TweetI";
	unlink $BleatsDirecRM;

	#Delete Blead Id from bleats.txt
	open $L, "<","$users_dir/$loggedin_User/bleats.txt" or die "can not open $users_dir/$loggedin_User/bleats.txt : $!";	
	chomp $L;
	@bleatToRM = <$L>;
	close $L;

	while(scalar(@bleatToRM) != 0){
		$BleatToRM = pop @bleatToRM;
		if($BleatToRM=~ m/$TweetI/){
			$BleatToRM=~ s/\w*//g;
		}
		chomp $BleatToRM;
		push(@RMDbleatFile,$BleatToRM);
	}
	open $K, ">","$users_dir/$loggedin_User/bleats.txt" or die "can not open $users_dir/$loggedin_User/bleats.txt : $!";
	chomp $K;	
	while(scalar(@RMDbleatFile)!=0){
		$NewBlFile = pop @RMDbleatFile;
		print $K "$NewBlFile\n";
	} 
	close $K;
}

sub edit_user_profile {
	$FirstName = param("FirstName");
	$FirstName=~ s/\W//g;
	$LastName = param("LastName");
	$LastName=~ s/\W//g;	
	$Email = param("Email");
	$Email =~ s/[\!\<\>\*\/\$\@]//g;	
	$CurrUserName = param("username");
	$CurrUserName=~ s/\W//;
	$PassWord = param("PassWord");
	$PassWord=~ s/\W//;
	$ConfirmPassWord = param("password");
	$ConfirmPassWord=~ s/\W//;	
	#$Submit = param("SubmitProfile");	

	$FullName = "full_name: $FirstName $LastName\n";
	$CurrUserName = "username: $CurrUserName\n";
	$CPassword = "$PassWord\n";
	$PassWord = "password: $PassWord\n";
	$Email = "email: $Email\n";
	
	#Edit Details.txt
	open $E,">", "$user_to_show/details.txt" or die "Can not open $user_to_show/details.txt $!";
	chomp $E;
	print $E "$FullName";
	print $E "$Email";
	print $E "$CurrUserName";
	print $E "$PassWord";
	close $E;

	#Edit password file
	open $Q, ">", "$user_to_show/password" or die "Can't open $user_to_show/password: $!";
	chomp $Q;
	print $Q "$CPassword";
	close $Q;

	#Change Pro Pic
	if(defined(param("ChangeProPic"))){
		$pic_path = "$users_dir/$loggedin_User/profile.jpg";
		$uploadPic = upload('ChangeProPic');
		open($pp,">",$pic_path) or die;
		binmode $pp;
		while($line = <$uploadPic>){
			$pic = print $pp $line;
		}
		close $pp;
	}

	#Change Cover Pic
	if(defined(param("ChangeCoverPic"))){
		$cover_path = "$users_dir/$loggedin_User/cover.jpg";
		$uploadCoverPic = upload('ChangeCoverPic');
		open($cp,">",$cover_path) or die;
		binmode $cp;
		while($line = <$uploadCoverPic>){
			$pic = print $cp $line;
		}
		close $cp;
	}

}

sub delete_user_account {
	$BleatsFile = "$users_dir/$loggedin_User/bleats.txt";
	$DetailsFile = "$users_dir/$loggedin_User/details.txt";
	$PasswordFile = "$users_dir/$loggedin_User/password";
	$ProfileTextFile = "$users_dir/$loggedin_User/profiletext.txt";
	$ProfilePicFile = "$users_dir/$loggedin_User/profile.jpg";
	$CoverPicFile = "$users_dir/$loggedin_User/cover.jpg";
	$BleatPicFile = "$users_dir/$loggedin_User/bleat.jpg";
	$DirectoryFolder = "$users_dir/$loggedin_User";

	open $R, "<","$users_dir/$loggedin_User/details.txt" or die "can not open $users_dir/$loggedin_User/details.txt :$!";
	$GetEmail = join "\n",<$R>;
	close $R;

	if($GetEmail=~ /email: (.*[aucom])/){
		$emailRec = $1;
	}
	open $E, "<","$users_dir/$loggedin_User/bleats.txt" or die "can not open $users_dir/$loggedin_User/bleats.txt : $!";
	@GetBID = <$E>;
	close $E;
	
	while(scalar(@GetBID)!=0){
		$DELid = pop @GetBID;
		$removeDelid = "$bleats_dir/$DELid";
		if(-e $removeDelid){
			unlink $removeDelid;
		} else {
			$DeleteBuffer = "$removeDelid has been deleted\n";
		}
	}
	if($emailRec eq param("Confirm Email")){
		if(-e $BleatsFile){
			unlink $BleatsFile;
		} else {
			$DeleteBuffer = "$BleatsFile has been deleted\n";
		}
		if(-e $DetailsFile){
			unlink $DetailsFile;
		} else {
			$DeleteBuffer = "$DetailsFile has been deleted\n";
		}
		if(-e $PasswordFile){
			unlink $PasswordFile;
		} else {
			$DeleteBuffer = "$PasswordFile has been deleted\n";
		}
		if(-e $ProfileTextFile){
			unlink $ProfileTextFile;
		} else {
			$DeleteBuffer = "$ProfileTextFile has been deleted\n";
		}
		if(-e $ProfilePicFile){
			unlink $ProfilePicFile;
		} else {
			$DeleteBuffer = "$ProfilePicFile has been deleted\n";
		}
		if(-e $CoverPicFile){
			unlink $CoverPicFile;
		} else {
			$DeleteBuffer = "$CoverPicFile has been deleted\n";
		}
		if(-e $BleatPicFile){
			unlink $BleatPicFile;
		} else {
			$DeleteBuffer = "$BleatPicFile has been deleted\n";
		}
		if(-e $DirectoryFolder){
			rmdir $DirectoryFolder;
		} else {
			rmdir $DirectoryFolder;
			$DeleteBuffer = "Account Has Been Deleted\n";
		}
		print "$DeleteBuffer\n";
	} else {
		print "Not correct Email Address\n";
		$cantpass = 1;
	}
}
sub profile_text {
	$NewProText = param("ProfileText");

	#Sanitize profile text	
	$NewProText =~ s/\W/ /g; 
	
	#Create text file
	$textfile = "$users_dir/$loggedin_User/profiletext.txt";
	open  $create_text_file, ">", "$textfile" or die "Can't open $textfile: $!";
	chomp $create_text_file;
	print $create_text_file "$NewProText";
	close $create_text_file;

	show_profile_text();
}

sub show_profile_text {

	open $T, "<","$users_dir/$loggedin_User/profiletext.txt" or die "Can't open $users_dir/$loggedin_User/profiletext.txt: $!";
	$ShowText = join "\n",<$T>;
	close $T;
}

sub static_nav_bar {
	open my $nav,"<", "$bootstrap_files/navbar-static-top/navbar-user.html" or die "cant open $bootstrap_files/navbar-static-top/navbar-user.html: $!";
	$nav_bar = join "\n",<$nav>;
	close $nav;
	print "$nav_bar\n";
}

sub cover_page {
	open my $cover,"<", "$bootstrap_files/cover/login.html" or die "cant open $bootstrap_files/cover/login.html: $!";
	$cover_page = join "\n",<$cover>;
	close $cover;
	print "$cover_page\n";
}

sub cover_pics {
	open my $coverpics,"<", "$bootstrap_files/carousel/coverpic.html" or die "cant open $bootstrap_files/carousel/coverpic.html: $!";
	$cover_pic = join "\n",<$coverpics>;
	close $coverpics;
	print "$cover_pic\n";
}

sub remove_following {
	
	#Delete Following name from details.txt
	open $N, "<","$users_dir/$loggedin_User/details.txt" or die "can not open $users_dir/$loggedin_User/details.txt : $!";	
	$followingToRM = <$L>;
	close $N;

	if($followingToRM =~ /($followerIs)/){
		$followingToRM =~ s/$1//;
	}

	open $B, ">","$users_dir/$loggedin_User/details.txt" or die "can not open $users_dir/$loggedin_User/details.txt : $!";
	print $B "$followingToRM\n"; 
	close $B;

}

sub add_following {
	open $D,">>","$users_dir/$loggedin_User/details.txt" or die "can not open $users_dir/$loggedin_User/details.txt: $!";
	print $D "listens: $FollowUser\n";
	close $D;
}

sub user_home_page {			
    return <<eof

<link class="cssdeck" rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.1/css/bootstrap.min.css">
<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.1/css/bootstrap-responsive.min.css" class="cssdeck">

<div class="container">
    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Bitter</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="#Home" data-toggle="tab">Home</a></li>
            <li><a href="#UserPage" data-toggle="tab"><span class="icon icon-chat"></span>$full_name</a></li>
			<li><a href="#Settings" data-toggle="tab">Settings</a></li>
			<li><a href="#DeleteAccount" data-toggle="tab">Delete Account</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
			<form method="POST" class="navbar-form navbar-left" role="search">
	  			<div class="form-group">
               <input type="text" class="form-control" name="username" placeholder="Search">
               <button class="btn btn-default" type="submit" name="password" value="$passWho">Search</button>
	  			</div>
			</form>
				<li class="dropdown">
              <a href="#Drop" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Logout<span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a href="#name">$username</a></li>
				 <li><a href="">Log Out</a></li>
              </ul>
            </li>
          </ul>
	</nav>
   </div><!--/.nav-collapse -->
  </div>

</div> <!-- /container -->  

<div class="container">
	<div id="TabContent" class="tab-content">
		<div class="tab-pane active in" id="UserPage">
			@current_user_page
		</div>
		<div class="tab-pane fade" id="Settings">
			@edit_Profile
		</div>
		<div class="tab-pane fade" id="Home">
			@current_home_page
		</div>
		<div class="tab-pane fade" id="DeleteAccount">
			@del_account
		</div>
	</div>
</div>
<script class="cssdeck" src="//cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

<script class="cssdeck" src="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>
eof
}

sub current_user_page {
	return<<user

		<div class="fb-profile">
		    <img align="left" class="fb-image-lg" src="$Cover_path" alt="Profile image example"/>
		    <img align="left" class="fb-image-profile thumbnail" src="$image_path" alt="Profile image example"/>
		    <div class="fb-profile-text">
			<form class="form-inline" role="form" method="POST">
				<div class="well">
				    <h1 class="name">$full_name</h1>
				    <h4 class="name">$user_name</h4>
					<h4 class="name">$ShowText</h4>
				<h4>Profile Text<h4>
				<div class="form-group">
					<input type="hidden" class="form-control" name="username" value="$username">
					<textarea type="text" class="form-control" name="ProfileText" rows="2" cols="40"></textarea>
					<button type="submit" name="password" value="$passWho" class="btn btn-default">Post</button>
				</div>
				<nav class="profile-header-nav">
					<ul class="nav nav-tabs">
					  <li class="active"><a href="#Bleats" data-toggle="tab">Bleats</a></li>
					  <li><a href="#Following" data-toggle="tab">Following</a></li>
					  <li><a href="#Followers" data-toggle="tab">Followers</a></li>
					</ul>
					<div id="myTabContent" class="tab-content">
						<div class="tab-pane active in" id="Bleats">
							<div class="panel-body" id="Bleats">
								<p class="bitter_user_bleat_details">@bleatsFile</p>
							</div>
						</div>
						<div class="tab-pane fade" id="Following">
							@displayfollowing
						</div>
						<div class="tab-pane fade" id="Followers">
							@displayfollowers
						</div>
					</div>
			  	</nav>	
				</div>
			</form>
		    </div>
		</div><!--/.fb-collapse -->
user
}

sub current_home_page {
	return<<home

	<div class="fb-profile">
		<div class="fb-profile-text">
		<form class="form-inline" role="form" method="POST">
			<div class="well">
				<br><br>
               <div class="form-group">
                  <label for="bleat">Bleat</label>
                     <div class="form-group">
						   <input type="hidden" class="form-control" name="username" value="$username">
                           <textarea type="text" class="form-control" name="newbleat" rows="2" cols="40" id="newbleat"></textarea>
						   <button type="submit" name="password" value="$passWho" class="btn btn-default">Bleat</button>
						   <div>
						      <input class="form-control" name="UploadBleatPic" type="file">
						   </div>
                           
                     </div>   
               </div>
				<div class="panel-body" id="Home">
					<p class="bitter_user_bleat_details">@HomeBleatsFile</p>
				</div>
			</div>
		 </form>
		</div>
	</div><!--/.fb-collapse -->

home
}

sub edit_profile {
	return<<edit 
<br><br><br>
<div class="panel-body">
	<div class="bitter_user_edit_details">
		<div class="container"> 
         <form method="POST" enctype="multipart/form-data">
         <h1>Edit Profile</h1>
            <div class="row">
               <!-- left column -->
               <div class="col-md-3">
                   <div class="text-center">
                       <img src="$image_path" class="avatar img-thumbnail img-responsive"
                       alt="avatar">
                        <h6>Upload a different photo...</h6>

                       <input class="form-control" name="ChangeProPic" type="file">
                   </div>
				   <br><br>
 				   <div class="text-center">
                       <img src="$Cover_path" class="avatar img-thumbnail img-responsive"
                       alt="avatar">
                        <h6>Upload a different photo...</h6>

                       <input class="form-control" name="ChangeCoverPic" type="file">
                   </div>
               </div>
               <!-- edit form column -->
               
               <div class="col-md-9 personal-info">
                    <h3>Personal info</h3>
                  <div class="form-group">
                       <label for="First Name" class="sr-only">First name:</label>
                       <div class="col-lg-8">
                           <input class="form-control" id="First Name" name="FirstName" value="" placeholder="First name" type="text" required autofocus>
                       </div>
                  </div>
                  <div class="form-group">
                       <label for="Last Name" class="sr-only">Last name:</label>
                       <div class="col-md-8">
                           <input class="form-control" id="Last Name" name="LastName" value="" placeholder="LastName" type="text" required autofocus>
                       </div>
                  </div>
                  <div class="form-group">
                       <label for="Email Add" class="sr-only">Email:</label>
                       <div class="col-md-8">
                           <input class="form-control" id="Email Add" name="Email" value="" placeholder="Email" type="text" required autofocus>
                       </div>
                  </div>
                  <div class="form-group">
                     <label for="Current Username" class="sr-only">Current Username:</label>
                       <div class="col-md-8">
                           <input class="form-control" id="Current Username" name="username" value="" placeholder="Current Username" type="text" required autofocus>
                       </div>
                  </div>
                  <div class="form-group">
                          <label for="Password" class="sr-only">Current PassWord:</label>
                          <div class="col-md-8">
                              <input id="Password" class="form-control"  name="password" value="$passWho" placeholder="Current Password" type="password" required autofocus>
                          </div>
                     </div>
                  <div class="form-group">
                       <label for="Confirm PassWord" class="sr-only">Confirm password:</label>
                       <div class="col-md-8">
                           <input class="form-control" id="password" name="PassWord" value="" placeholder="New/Confirm Password" type="password" required autofocus>
                       </div>
                  </div>
                  <div class="form-group">
                       <label for="SubmitProfile" class="sr-only"></label>
                       <div class="col-md-8">
                           <button class="btn btn-default" id="SubmitProfile" type="submit">SaveChanges</button>
                       </div>
                  </div>

               </div>
            </div>
     
			</form>
		</div> <!-- /container --> 
		<br>
	</div>
</div>
edit
}

sub delete_account {
	return<<deleteA

<br><br><br>
<div class="panel-body">
	<div class="bitter_user_edit_details">
		<div class="container"> 
			<form method="POST">
				<div class="col-md-9 personal-info">
					<h4>Delete Bitter Profile</h4>
					<div class="form-group">
					<div class="form-group">
						<label for="Email Add" class="sr-only">Email:</label>
						<div class="col-md-8">
						   <input class="form-control" id="Email Add" name="Confirm Email" value="" placeholder="Email" type="text" required autofocus>
						</div>
					</div>
						<label for="Current Username" class="sr-only">Current Username:</label>
						<div class="col-md-8">
						   <input class="form-control" id="Current Username" name="username" value="" placeholder="Current Username" type="text" required autofocus>
						</div>
					</div>
					<div class="form-group">
						<label for="Password" class="sr-only">Current PassWord:</label>
						<div class="col-md-8">
						  <input id="Password" class="form-control"  name="password" value="$passWho" placeholder="Current Password" type="password" required autofocus>
						</div>
					</div>
					<div class="form-group">
						<label for="SubmitProfile" class="sr-only"></label>
						<div class="col-md-8">
						   <button class="btn btn-danger" id="DeleteProfile" type="submit">Delete Account</button>
						</div>
					</div>
				</div>
			</form>
		</div> <!-- /container --> 
	</div>
</div>

deleteA
}

sub confirm_delete {
	return<<confirmDel

<br><br><br>
<div class="panel-body">
	<div class="bitter_user_edit_details">
 		<a href="" type="button">Delete Account</a></button>
	</div>
</div>

confirmDel
}
#HTML code for Display followers in user page
sub display_followers {
					return<<end

<link href="bootstrap-3.3.5/dist/css/bootstrap.min.css" rel="stylesheet">
<ul class="media-list media-list-users list-group">
  <li class="list-group-item">
    <div class="media">
      <a class="media-left" href="#">
        <img class="media-object img-circle" data-action="zoom" style="width: 80px;" src="$followerImage_path">
      </a>
      <div class="media-body">       
        <strong>$followerName</strong>
        <small>\@$followerIs</small> 
      </div>
    </div>
  </li>
</ul>
end
}

#HTML code for Display following in user page
sub display_following {
					return<<end

<link href="bootstrap-3.3.5/dist/css/bootstrap.min.css" rel="stylesheet">
<ul class="media-list media-list-users list-group">
  <li class="list-group-item">
    <div class="media">
      <a class="media-left" href="#">
        <img class="media-object img-circle" data-action="zoom" style="width: 80px;" src="$followingImage_path">
      </a>
      <div class="media-body">    
        <strong>$followingName</strong>
        <small>\@$followingIs</small>
		<form method="POST">
	    <input type="hidden" class="form-control" name="username" value="$username">
	    <input type="hidden" class="form-control" name="password" value="$passWho">
	    <input type="submit" class="btn btn-primary btn-sm pull-right" name="Listening" value="Following">
		</form>
      </div>
    </div>
  </li>
</ul>
end
}



#HTML Code for displaying bleats
sub display_bleats {
	$n = $n + 1;
	$i = $i + 1;

	return<<bleats
<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
<div class="panel panel-default">
<div class="media">
      <a class="media-left" href="#">
        <img class="media-object img-circle" data-action="zoom" style="width: 40px;" src="$image_path">
      </a>
 <div class="media-body">
	<form method="POST" class="form-inline">
	   <strong>$full_name</strong>
       <small>$user_name</small>
	   <input type="hidden" class="form-control" name="username" value="$username">
	   <input type="hidden" class="form-control" name="password" value="$passWho">
	   <input type="submit" class="btn btn-danger pull-right" name="DeleteTweet" value="Delete">
	</form>
    <div class="panel-heading" role="tab" id="heading$i">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse$n" aria-expanded="false" aria-controls="collapse$n">
          $bleats
		@displayIM
        </a>
      </h4>
    </div>
 <div id="collapse$n" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading$i">
      <div class="panel-body">
    @ReplyUsrBleat
	@ReplyUsArBleat
      </div>
    </div>

   </div>
    </div>
  </div>
</div>
bleats
}

sub display_image_bleats{
	return<<imb

	<img class="media-obeject img-thumbnail" src="$Bleat_Img">

imb
}

sub display_reply_bleats {
	return<<replybleat

<div class="media">
      <a class="media-left" href="#">
        <img class="media-object img-circle" data-action="zoom" style="width: 40px;" src="$BleatImage_path">
      </a>
 <div class="media-body">
	   <strong>$followerReplyName</strong>
        <small>\@$GetBleatUname</small>
    <div class="panel-heading" role="tab" id="heading$i">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse$n" aria-expanded="false" aria-controls="collapse$n">
          $bleatRep
        </a>
      </h4>
    </div>    
   </div>
    </div>

replybleat
}

sub display_home_bleat {
	$x = $x + 1;
	$y = $y + 1;
	return<<hbleats
<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
<div class="panel panel-default">
<div class="media">
      <a class="media-left" href="#">
        <img class="media-object img-circle" data-action="zoom" style="width: 40px;" src="$followerHomeImage_path">
      </a>
 <div class="media-body">
	   <strong>$followerHomeName</strong>
        <small>\@$GetUname</small>
    <div class="panel-heading" role="tab" id="heading$y">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse$x" aria-expanded="true" aria-controls="collapse$x">
          $HomeBleats
        </a>
      </h4>
    </div>
	<div id="collapse$x" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading$y">
      <div class="panel-body">
		@ReplyHomeBleat
		@ReplyHomereplyBleat
      </div>
    </div>

   </div>
    </div>
  </div>
</div>
hbleats
}

sub display_home_reply_bleat {
	return<<hrbleat

<div class="media">
      <a class="media-left" href="#">
        <img class="media-object img-circle" data-action="zoom" style="width: 40px;" src="$BleatHomeImage_path">
      </a>
 <div class="media-body">
	   <strong>$followerHomeReplyName</strong>
        <small>\@$GetBleatHUname</small>
    <div class="panel-heading" role="tab" id="heading$y">
      <h4 class="panel-title">
        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse$x" aria-expanded="false" aria-controls="collapse$x">
          $bleatHRep
        </a>
      </h4>
    </div>    
   </div>
    </div>

hrbleat
}
main();
