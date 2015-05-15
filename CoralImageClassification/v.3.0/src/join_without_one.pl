#!/usr/bin/perl -w
#

use strict;
my @all = qw[EKC ELH1 ELH2 LHM5 NKH1 NKH2 NKH3 WLH1 WLH2];
for my $i (0 .. $#all) {
	my $not = $all[$i];
	open(OUT, ">all_not_".$not.".txt") || die "Can't write to $not";
	my $header; my $thisheader;
	for my $j (0 .. $#all) {
		next if ($i == $j);
		open(IN, "$all[$j].data.txt") || die "can't open $all[$j].data.txt";
		$thisheader = <IN>;
		chomp($thisheader);
		$thisheader =~ s/\t$//;
		if (not defined $header) {
			$header = $thisheader;
			print OUT $header, "\n";
		}
		if ($thisheader ne $header) {print STDERR "WARNING: Header in $all[$j].data.txt is different\n"}
		while (<IN>) {
			chomp;
			s/\t$//;
			print OUT "$_\n";
		}
		close IN;
	}
	close OUT;
	#print STDERR "Running R and random forests with all_not_${not}.txt\n";
	#push @pids, $rob->background_job("Rscript ../src/randomForestTrainPredictNoTrim.r all_not_${not}.txt > rf_output/all_not_${not}.rf.output.txt");
	print "Rscript ../src/randomForestTrainPredictNoTrim.r all_not_${not}.txt > rf_output/all_not_${not}.rf.output.txt &\n";
}

