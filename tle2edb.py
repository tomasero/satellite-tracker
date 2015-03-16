#!/usr/bin/python
# tle2edb.py: Python port of the perl script of the same name. 
#
# The text below is the comments and license of the software
# tle2edb.pl: perl script to convert NASA "2-line" geocentric orbital elements
# to XEphem .edb. we crack everything that looks reasonable. we allow the TLE
# to be embedded in other text, just so long as it stands on three successive
# lines of their own. the idea is to keep rolling successive lines into l1,
# l2 and l3 and crack whenever they all look correct.
#
# (c) 1993,1995,1998,2000 Elwood Charles Downey
#
# v2.2  9/22/00 add drag term
# v2.1  12/8/98 change to perl. actually use the checksum. support Y2K.
# v2:   6/26/95 allow names up to 22 chars long (official format change).
# v1.3 10/26/93 looks even harder.
# v1.2  9/12/93 fixes for NORAD-format (by bon@LTE.E-TECHNIK.uni-erlangen.de)
# v1.1   9/8/93 change type code to E
# v1.0  8/10/93 initial cut
#
# usage:
#	tle2edb.pl [file]
#
# Data for each satellite consists of three lines in the following format:
#
# AAAAAAAAAAAAAAAAAAAAAA
# 1 NNNNNU NNNNNAAA NNNNN.NNNNNNNN +.NNNNNNNN +NNNNN-N +NNNNN-N N NNNNN
# 2 NNNNN NNN.NNNN NNN.NNNN NNNNNNN NNN.NNNN NNN.NNNN NN.NNNNNNNNNNNNNN
#
# Line 0 is a 22-character name.
#
# Lines 1 and 2 are the standard Two-Line Orbital Element Set Format identical
# to that used by NORAD and NASA.  The format description is:
#
# Line 1
# Column     Description
#  01-01     Line Number of Element Data
#  03-07     Satellite Number
#  10-11     International Designator (Last two digits of launch year)
#  12-14     International Designator (Launch number of the year)
#  15-17     International Designator (Piece of launch)
#  19-20     Epoch Year (Last two digits of year). 2000+ if < 57.
#  21-32     Epoch (Julian Day and fractional portion of the day)
#  34-43     First Time Derivative of the Mean Motion
#         or Ballistic Coefficient (Depending on ephemeris type)
#  45-52     Second Time Derivative of Mean Motion (decimal point assumed;
#            blank if N/A)
#  54-61     BSTAR drag term if GP4 general perturbation theory was used.
#            Otherwise, radiation pressure coefficient.  (Decimal point assumed)
#  63-63     Ephemeris type
#  65-68     Element number
#  69-69     Check Sum (Modulo 10)
#            (Letters, blanks, periods, plus signs = 0; minus signs = 1)
#
# Line 2
# Column     Description
#  01-01     Line Number of Element Data
#  03-07     Satellite Number
#  09-16     Inclination [Degrees]
#  18-25     Right Ascension of the Ascending Node [Degrees]
#  27-33     Eccentricity (decimal point assumed)
#  35-42     Argument of Perigee [Degrees]
#  44-51     Mean Anomaly [Degrees]
#  53-63     Mean Motion [Revs per day]
#  64-68     Revolution number at epoch [Revs]
#  69-69     Check Sum (Modulo 10)
#
# All other columns are blank or fixed.
#
# Example:
#
# NOAA 6
# 1 11416U          86 50.28438588 0.00000140           67960-4 0  5293
# 2 11416  98.5105  69.3305 0012788  63.2828 296.9658 14.24899292346978
# 
# Should yield:
#
# NOAA 6-529,E,1/ 50.28438588/1986, 98.5105, 69.3305,0.0012788, 63.2828,296.9658,14.24899292,0.00000140,34697
#
import sys
l1 = str(sys.argv[1])
l2 = str(sys.argv[2]) 
l3 = str(sys.argv[3])

if len(l1) > 22:
	exit()
#elif (!checksum(l2) and !checksum(l3)):
#	exit()
	
# $l1 is just the satellite name
name = l1
# pick out the goodies from l2, "line 1" of the TLE
year = int(l2[18:20])
if (year >= 57):
    year += 1900 
else:
    year += 2000
dayno = l2[20:32]

decay = l2[34:44]
drag = l2[54:55] + str(float(l2[55:59]) * pow(10, float(l2[60:62]) * 1e-5))
set0 = l2[65:68]

# pick out the goodies from l3, "line 2" of the TLE
inc = l3[8:16]
ra = l3[17:25]
e = float(l3[26:33]) * 1e-7
ap = l3[34:42]
anom = l3[43:51]
n = l3[52:63]
rev = l3[63:68]

# print in xephem format.
print "%s-%s,E,1/%s/%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (name, set0, dayno, year, inc, ra, e, ap, anom, n, decay, rev, drag)

''' TODO port from perl (3/16/2015)
sub chksum
{
    my $line = $_[0];
    my $len = length($line);
    my ($sum, $i, $c);

    $sum = 0;
    for ($i = 1; $i < $len; $i++) {
	$c = substr($line,$i,1);
	$sum += $c if ($c =~ /[\d]/);
	$sum += 1 if ($c eq "-");
    }
    $c = substr($line,$len,1);
    return (($sum % 10) == $c);
}
*/'''