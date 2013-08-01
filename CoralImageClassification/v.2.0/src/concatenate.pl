#!/usr/bin/perl -w
#

use strict;
my $header;
foreach my $f (@ARGV) {
	open(IN, $f) || die "Can't open $f";
	$f =~ s/.all.features.txt//;
	my $thisheader=0;
	while (<IN>) {
		if ($header && !$thisheader) {
			if ($_ ne $header) {print STDERR "WARNING: $f appears to have different columns\n"}
			$thisheader=1;
			next;
		}
		elsif (!$thisheader) {
			$header=$_; 
			print;
			$thisheader=1;
			next;
		}
		print $f, "/", $_;
	}
	close IN;

}
