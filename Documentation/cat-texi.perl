#!/usr/bin/perl -w

use strict;
use warnings;

my @menu = ();
my $output = $ARGV[0];

open my $tmp, '>', "$output.tmp";

while (<STDIN>) {
	next if (/^\\input texinfo/../\@node Top/);
	next if (/^\@bye/ || /^\.ft/);
	if (s/^\@top (.*)/\@node $1,,,Top/) {
		push @menu, $1;
	}
	s/\(\@pxref\{\[(URLS|REMOTES)\]}\)//;
	s/\@anchor\{[^{}]*\}//g;
	print $tmp $_;
}
close $tmp;

print '\input texinfo
@setfilename stgitman.info
@documentencoding UTF-8
@dircategory Development
@direntry
* StGit Man Pages: (stgitman).  Manual pages for StGit
@end direntry
@node Top,,, (dir)
@top StGit Manual Pages
@documentlanguage en
@menu
';

for (@menu) {
	print "* ${_}::\n";
}
print "\@end menu\n";
open $tmp, '<', "$output.tmp";
while (<$tmp>) {
	print;
}
close $tmp;
print "\@bye\n";
unlink "$output.tmp";
