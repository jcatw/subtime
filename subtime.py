#!/usr/bin/env python
# Add or subtracts an offset from a .srt-formatted subtitle file
#  arg1: input file name
#  arg2: offset of form hh:mm:ss,mss or -hh:mm:ss,mss
#  arg3: output file
#
# Author: James Atwood
# Email: jatwood@cs.umass.edu
# Written: 4/3/13
# Why: Spanish horror overdubs just can't quite measure up
# 
# nptime was written by Thomas Grenfell Smith <thomathom@gmail.com>
#
# Released under the MIT license; see LICENSE for details.
# 
from datetime import time, timedelta
import nptime as npt
import re
import sys

def main(input_file, offset_string, output_file):
    subtract = False
    
    if offset_string[0] == '-':
        subtract = True
        offset_string = offset_string[1:]

    offset_match = re.match("([0-9]{2}):([0-9]{2}):([0-9]{2}),([0-9]{3})", offset_string)
    
    
    if offset_match is None:
        print "Malformed offset: %s" % offset_string
        print "Expected forms: hh:mm:ss,mss or -hh:mm:ss,mss"
        sys.exit()
        
    offset_groups = offset_match.groups()
    offset_time = timedelta(hours=int(offset_groups[0]),
                            minutes=int(offset_groups[1]),
                            seconds=int(offset_groups[2]),
                            microseconds=1000 * int(offset_groups[3]))  #goes straight to microseconds from seconds(?!)

    subout = open(output_file, 'w')
    for line in open(input_file, 'r'):
        line = line.strip()

        #matches a timestamp and extracts
        #h1, m1, s1, ms1, h2, m2, s2, ms2
        timestamp_match = re.match("([0-9]{2}):([0-9]{2}):([0-9]{2}),([0-9]{3}) --> ([0-9]{2}):([0-9]{2}):([0-9]{2}),([0-9]{3})",line)

        
        
        if not timestamp_match is None:
            timestamp_groups = timestamp_match.groups()
            
            time1 = npt.nptime(int(timestamp_groups[0]),
                         int(timestamp_groups[1]),
                         int(timestamp_groups[2]),
                         1000 * int(timestamp_groups[3]))  #goes straight to microseconds from seconds(?!)
            time2 = npt.nptime(int(timestamp_groups[4]),
                         int(timestamp_groups[5]),
                         int(timestamp_groups[6]),
                         1000 * int(timestamp_groups[7]))

            if subtract:
                td1 = time1 - offset_time  #subtraction returns a timedelta ARARRRRGHAAGwb WHY
                td1_hours = int(td1.seconds) / 3600
                td1_minutes = int(td1.seconds - 3600 * td1_hours) / 60
                td1_seconds = int(td1.seconds - 3600 * td1_hours - 60 * td1_minutes)
                time1 = time(td1_hours,
                             td1_minutes,
                             td1_seconds,
                             td1.microseconds)

                
                td2 = time2 - offset_time
                td2_hours = int(td2.seconds) / 3600
                td2_minutes = int(td2.seconds - 3600 * td2_hours) / 60
                td2_seconds = int(td2.seconds - 3600 * td2_hours - 60 * td2_minutes)
                time2 = time(td2_hours,
                             td2_minutes,
                             td2_seconds,
                             td2.microseconds)
                    
                
            else:
                time1 = time1 + offset_time  #but addition returns nptime
                time2 = time2 + offset_time  
            
            # strftime milliseconds seem kind of fucked,
            # so just use a format string
            subout.write("%02d:%02d:%02d,%s --> %02d:%02d:%02d,%s" % (time1.hour,
                                                                      time1.minute,
                                                                      time1.second,
                                                                      int(str(time1.microsecond)[:3]),
                                                                      time2.hour,
                                                                      time2.minute,
                                                                      time2.second,
                                                                      int(str(time2.microsecond)[:3])))
            subout.write("\n")
        else:
            subout.write(line)
            subout.write("\n")
                    
    subout.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'usage: input_file.srt [-]hh:mm:ss,mss output_file.srt'
        sys.exit()
    main(*sys.argv[1:])
