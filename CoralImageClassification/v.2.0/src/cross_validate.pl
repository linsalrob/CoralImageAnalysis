#!/usr/bin/perl -w
#

use strict;

my $allf = shift || die "All data file that has categories in column 1";
my $dir = shift || die "directory with crossTest probability outputs";
my $outf = shift || die "file to write to";
open(OUT, ">$outf") || die "can't write to $outf";

open(IN, $allf) || die "Can't open $allf";
my %known;
while (<IN>) {
	chomp;
	s/^.*?\///; # trim off the data type at the beginning
	my @a=split /\t/;
	$a[1] =~ s/\./ /g;
	$known{$a[0]} = $a[1] if ($a[1] ne "Unknown");
}
close IN;


opendir(DIR, $dir) || die "Can't open $dir";
my %allrfs; my $crossvalidation;
foreach my $f (sort {$a cmp $b} grep {$_ !~ /^\./} readdir(DIR)) {
	if ($f =~ /\.gz$/) {
		open(IN, "gunzip -c $dir/$f |") || die "can't open a pipe to gunzip -c $dir/$f";
	} else {
		open(IN, "$dir/$f") || die "Can't open $dir/$f";
	}
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
	$f =~ /([\w\.]+)_data.([\w\.]+)_rf/;
	my ($ds, $rfs)=($1, $2);
	print OUT "\n\nUsing the random forest trained on $rfs and data set $ds. The number of images classified was: $count. The number correctly assigned was: $correct (";
	print OUT sprintf("%0.2f", ($correct/$count)*100);
	print OUT " % correct)\n";

	$crossvalidation->{$ds}->{$rfs}=sprintf("%0.2f", ($correct/$count)*100);
	$allrfs{$rfs}=1;

	print OUT join("\t", "", @t), "\n";
	foreach my $i (@t) {
		print OUT $i;
		map {
		if ($expect->{$i}->{$_}) {print OUT "\t", $expect->{$i}->{$_}}
		else {print OUT "\t0"}
		} @t;
		print OUT "\n";
	}
}


print OUT "=" x 30;
print OUT "\n\n";
my @arfs=sort {$a cmp $b} keys %allrfs;
print OUT "\t\t\tRANDOM FORESTS\n";
print OUT join("\t", "", @arfs), "\n";
foreach my $a (@arfs) {
	print OUT $a;
	map {
		if ($crossvalidation->{$a}->{$_}) {print OUT "\t", $crossvalidation->{$a}->{$_}}
		else {print OUT "\t0"}
	} @arfs;
	print OUT "\n";
}

