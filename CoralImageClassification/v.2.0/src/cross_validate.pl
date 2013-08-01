#!/usr/bin/perl -w
#

use strict;

open(IN, "all.data.txt") || die "Can't open all.data.txt";
my %known;
while (<IN>) {
	chomp;
	s/^.*?\///; # trim off the data type at the beginning
	my @a=split /\t/;
	$a[1] =~ s/\./ /g;
	$known{$a[0]} = $a[1] if ($a[1] ne "Unknown");
}
close IN;


opendir(DIR, "cross_test_probabilities") || die "Can't open cross_test_probabilities";
my %allrfs; my $crossvalidation;
foreach my $f (sort {$a cmp $b} grep {$_ !~ /^\./} readdir(DIR)) {
	open(IN, "cross_test_probabilities/$f") || die "Can't open $f";
	my $header;
	my $count=0;
	my $correct=0;
	my $expect;
	my %alltypes;
	while (<IN>) {
		chomp;
		s/\"//g;
		unless ($header) {
			s/\./ /g; 
			my @a=split /\t/;
			$header=\@a; 
			next;
		}
		my @a=split /\t/;
		if (!defined $known{$a[1]}) {$a[1] =~ s/^.*?\///}
		next unless ($known{$a[1]});
		$count++;

		my $max=0;
		my $type;
		map {if ($a[$_] > $max) {$max=$a[$_]; $type=$header->[$_-1]}} (2 .. $#a);
		$expect->{$known{$a[1]}}->{$type}++;
		if ($known{$a[1]} eq $type) {$correct++}
		$alltypes{$type}=1;
		$alltypes{$known{$a[1]}}=1;
	}
	unless ($count) {die "There were no knowns in $f"}

	my @t=sort {$a cmp $b} keys %alltypes;
	$f =~ /(\w+)_data.(\w+)_rf/;
	my ($ds, $rfs)=($1, $2);
	print "\n\nUsing the random forest trained on $rfs and data set $ds. The number of images classified was: $count. The number correctly assigned was: $correct (";
	printf("%0.2f", ($correct/$count)*100);
	print " % correct)\n";

	$crossvalidation->{$ds}->{$rfs}=sprintf("%0.2f", ($correct/$count)*100);
	$allrfs{$rfs}=1;

	print join("\t", "", @t), "\n";
	foreach my $i (@t) {
		print $i;
		map {
		if ($expect->{$i}->{$_}) {print "\t", $expect->{$i}->{$_}}
		else {print "\t0"}
		} @t;
		print "\n";
	}
}


print "=" x 30;
print "\n\n";
my @arfs=sort {$a cmp $b} keys %allrfs;
print "\t\t\tRANDOM FORESTS\n";
print join("\t", "", @arfs), "\n";
foreach my $a (@arfs) {
	print $a;
	map {
		if ($crossvalidation->{$a}->{$_}) {print "\t", $crossvalidation->{$a}->{$_}}
		else {print "\t0"}
	} @arfs;
	print "\n";
}

