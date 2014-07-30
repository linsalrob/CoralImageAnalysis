#!/usr/bin/perl -w
#
use strict;

my $file=shift || die "features file";
open(IN, $file) || die "Can't open $file";
my $header; my $data;
my $m=0;
while (<IN>) {
	chomp;
	my @a=split /\t/;
	my $if = shift @a;
	($m < $#a) ? ($m=$#a) : 1; # does not include file name
	unless ($header) {$header=join("\t", @a); next}
	$data->{$if}=\@a;
}
close IN;
my $file2=shift || die "all analysis file";
open(IN, $file2) || die "Can't open $file2";
while (<IN>) {
	chomp;
	s/\t$//;
	if ($header) {
		print "$_\t$header\n";
		undef $header;
		next;
	}
	my @a=split /\t/;
	if ($data->{$a[0]}) {
		unless ($#{$data->{$a[0]}} == $m) {$#{$data->{$a[0]}} = $m}
		print join("\t", $_, @{$data->{$a[0]}}), "\n";
	}
	else {
		print STDERR "No data for $a[0]\n";
		my @empty;
		$#empty=$m;
		print join("\t", $_, @empty), "\n";
	}
}
close $file2;
