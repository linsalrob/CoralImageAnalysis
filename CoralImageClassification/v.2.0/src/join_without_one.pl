#!/usr/bin/perl -w
#

use strict;
my @all=qw[ELH1 ELH2 LHM5 WLH1 WLH2];
for my $i (0 .. 4) {
	my $not = $all[$i];
	open(OUT, ">all_not_".$not.".txt") || die "Can't write to $not";
	my $header; my $thisheader;
	for my $j (0 .. 4) {
		next if ($i == $j);
		open(IN, "$all[$j].data.txt") || die "can't open $all[$j].data.txt";
		$thisheader = <IN>;
		if (not defined $header) {
			$header = $thisheader;
			print OUT $header;
		}
		if ($thisheader ne $header) {print STDERR "WARNING: Header in $all[$j].data.txt is different\n"}
		print OUT while (<IN>);
		close IN;
	}
	close OUT;
	print STDERR "Running R and random forests with all_not_${not}.txt\n";
	system("Rscript ../src/randomForestTrainPredictNoTrim.r all_not_${not}.txt > all_not_${not}.rf.output.txt");
}

