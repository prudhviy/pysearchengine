#!/usr/bin/perl
##
## fixedredir.cgi

use strict;
use warnings;


my $URL = "http://www.bsdpython.org/";

print "Status: 302 Moved\nLocation: $URL\n\n";
