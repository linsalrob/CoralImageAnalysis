#!/usr/bin/perl -w
#

use strict;
my $infile = shift || die "input file";
my $outfile = shift || die "output file";
open(IN, $infile) || die "Can't open $infile";
my $max=0;
while (<IN>) {
	chomp;
	my @a=split /\t/;
	($max < $#a) ? ($max=$#a) : 1;
}
close IN;
open(IN, $infile) || die "Can't open $infile";
open(OUT, ">$outfile") || die "Can't open $outfile";
while (<IN>) {
	chomp;
	my @a=split /\t/;
	if ($#a != $max) {
		print STDERR "$a[0] only has $#a columns. Fixed\n";
		$#a=$max;
	}
	if ($a[1] eq "") {$a[1] = "Unknown"}
	map {$a[$_] = 0 unless (defined $a[$_])} (2 .. $#a);
	print OUT join("\t", @a), "\n";
}
