# SSIM_remap part of the SSIM_utils
# Copyright 2026 Stefano Sinagra sinager@tarapippo.net

''' Utility will rename flight numbers into a SSIM file according to a
    map stored into a csv file.
    Example entry in mapping file: XX0123,YY0789
    Flight XX0123 will be changed into flight YY0789
    Original operating interval can be overwritten to new dates.
    You can choose whether to keep in output file non remapped flights. 
    Output will be saved in a [hopefully] compliant SSIM file
    v 1.0 March 2026
'''

''' This file is part of SSIM_utils https://github.com/Sinager/SSIM_utils
    SSIM_utils is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

import argparse

cxorig = ''
cxremap = ''
fltorig = ''
fltnew = ''
fltmap = {}
perstart = ''
perend = ''

parser = argparse.ArgumentParser(description ='Utility to perform simple changes on SSIM files.')

parser.add_argument('inputfile', help='inputfile.ssim')
parser.add_argument('outputfile', help='outputfile.ssim')
parser.add_argument('-m','--mapflights',help='CSV file containing flight numbers to be remapped. Es. XX0123,YY0789')
parser.add_argument('-p','--period',help='comma separated time interval to owerwrite existing one. Es. 18SEP26,31JAN26')
parser.add_argument('-k','--keep', action='store_true', help='keep non code mapped flights in output, otherwise they will be discarded')
parser.add_argument('-c','--credits',help='SSIM utilities - Copyright 2026 Stefano Sinagra released under GPLv3 ')

args = parser.parse_args()
print(args)
infilename = args.inputfile

# if a flight renaming operation is requested, ingest the CSV mapping
# example: QJ1456,AZ9591,# Orig JFK  <-- third field is just a comment and not used
if args.mapflights:
    f = open(args.mapflights)
    fltlist = f.readlines()
    for flt in fltlist:
        fltmap[flt.split(",")[0]] = flt.rstrip('\n').split(",")[1]        

# if a date change is requested, make small checks on dates (5 chars each, capitalized)
if args.period:
    if len(args.period) == 15:
        period = args.period.split(',')
        perstart = period[0].upper()
        perend = period[1].upper()
    else:
        print('Invalid dates specification')
        quit()


with open(infilename) as infile:
    print('Scanning file...')
    outfilename = args.outputfile
    outfile= open(outfilename, 'w')
    linecount = 0
    for line in infile:
        # Record Type 1 > we copy as is to output file 
        if line[0] == '1':
            print('Header')
            print(line)
            outfile.write(line)
            linecount += 1
        if line[0:5] == '00000':
            #print('padding')
            outfile.write(line)
        # Record Type 2 > date change must be set here as well
        if line[0] == '2':
            print('Carrier Record')
            if args.period:
                line = line[0:14] + perstart + perend + line[28:]
            print(line)
            outfile.write(line)
            linecount += 1
        # Record Type 3 > filters are applied
        if line[0] == '3':
            cxorig = line[2:4]
            fltorig = line[5:9]
            origsvc = cxorig + fltorig
            # flight number remapping
            # date change
            if args.period:
                line = line[0:14] + perstart + perend + line[28:]
            if args.mapflights and origsvc in fltmap:
                print(origsvc, end=' remapping to: ')
                destsvc = fltmap[origsvc]              
                cxremap = destsvc[0:2]
                fltnew = destsvc[2:7]
                print(destsvc)
                line = "3 " + cxremap + " " + fltnew + line[9:]
                # line renumbering
                linecount += 1
                outline = line[0:194] + str(linecount).zfill(6) + '\n'
                print(outline)
                outfile.write(outline)                
            else:
                if args.keep:
                    print(origsvc, end=' no flt change, keep as is\n')
                    # line renumbering
                    linecount += 1
                    outline = line[0:194] + str(linecount).zfill(6) + '\n'
                    print(outline)
                    outfile.write(line)
                else:
                    print(origsvc, end=' no flt change, discarding\n')
            
        # Record Type 5 > we copy as is to output file                    
        if line[0] == '5':
            print('Trailer Record')
            # line renumbering
            outline = line[0:187] + str(linecount).zfill(6) + 'E' + str(linecount+1).zfill(6) + '\n'
            outfile.write(outline)
            linecount += 1
            
    outfile.close()
    infile.close()

    
