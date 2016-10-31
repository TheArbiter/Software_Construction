#!/bin/sh

# Run from webserver.sh to handle a single http request
# written by andrewt@cse.unsw.edu.au as a COMP2041 example

read http_request || exit 1

status_line="HTTP/1.0 200 OK"
content_type="text/plain"
content="Hi, I am a shell webserver and I received this HTTP request: $http_request"
content_length=`echo "$content"|wc -c`

echo "HTTP/1.0 200 OK"
echo "Content-type: $content_type"
echo "Content-length: $content_length"
echo
echo "$content"
exit 0
