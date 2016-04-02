# Copyright (c) 2016 Joseph Lenox
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import re

parser = argparse.ArgumentParser(description='Convert gcode with on/off to smoothieware laser.')
parser.add_argument('files', metavar='N', type=str, nargs='+',
                   help='gcode file')

args = parser.parse_args()

pwron = re.compile("M106 S([0-9]*)")
pwroff = re.compile("M107 S([0-9]*)")
gcode_regex = re.compile("([GM])([0-9]*)(.*)")
gcode_regex_single = re.compile("([GM])([0-9]*)")
for f in args.files:
  outname = "smoothie-" + f
  with open(f, 'r') as infile:
    outfile = open(outname, 'w');
    is_on = False
    power = 0.0
    for line in infile:
      if re.match(pwron, line):
        power = int(re.match(pwron, line).groups(0)[0]) / 256.0;
        is_on = True
        continue
      if re.match(pwroff, line):
        is_on = False
        power = int(re.match(pwroff, line).groups(0)[0]);
        continue
      if is_on:
        """ Process this gcode. """
        print line
        if re.match(gcode_regex, line):
          res = re.match(gcode_regex, line).groups()
          if res[1] in ['0', '1', '2', '3']:
            if res[1] in ['0', '1']:
              outfile.write("G1" + res[2] + " S" + str(power) + "\n")
            else:
              outfile.write(re.sub("\n", "", line) + " S" + str(power) + "\n")
          else:
            outfile.write(line)
        else:
            outfile.write(line)
      else:
        if re.match(gcode_regex, line):
          res = re.match(gcode_regex, line).groups()
          if res[1] in ['0', '1']:
            outfile.write("G0" + res[2] + "\n")
          else:
            outfile.write(line)
            

    outfile.close()
