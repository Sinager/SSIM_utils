# SSIM_filter part of the SSIM_utils
# Copyright 2026 Stefano Sinagra sinager@tarapippo.net

''' Utility will process a SSIM file filtering only services we are interested in.
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

filterhub = False
filterorig = False
filterdest = False
filterflight = False
legorig = ''
legdest = ''
legflight = ''
hub = ''

parser = argparse.ArgumentParser(description ='Utility to filter SSIM files.')

parser.add_argument('inputfile', help='inputfile.ssim')
parser.add_argument('outputfile', help='outputfile.ssim')
parser.add_argument('-o','--origins',help='departure station(s). Es. JFK,BOS')
parser.add_argument('-d','--destinations',help='arrival station(s). Es. IAD,MIA')
parser.add_argument('-f','--flights',help='flight number(s). Es. 9564,1322')
parser.add_argument('-s','--station',help='list flights in/out of a hub. May not work in conjunction with other options Es. BOS')
parser.add_argument('-c','--credits',help='SSIM utilities - Copyright 2026 Stefano Sinagra released under GPLv3 ')


args = parser.parse_args()
print(args)
infilename = args.inputfile

if args.station:
    hub = args.station
    print('Filtering by hub: ',end='')
    print(hub)
    filterhub = True

if args.origins:
    origins = args.origins.split(',')
    print('Filtering by origin: ',end='')
    print(origins)
    filterorig = True
    
if args.destinations:
    destinations = args.destinations.split(',')
    print('Filtering by destination: ',end='')
    print(destinations)
    filterdest = True

if args.flights:
    flights = args.flights.split(',')
    print('Filtering by flight: ',end='')
    print(flights)
    filterflight = True

with open(infilename) as infile:
    print('Scanning file...')
    linecount = 0
    outfilename = args.outputfile
    outfile= open(outfilename, 'w')
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
        # Record Type 2 > we copy as is to output file
        if line[0] == '2':
            print('Carrier Record')
            print(line)
            outfile.write(line)
            linecount += 1
        # Record Type 3 > filters are applied
        if line[0] == '3':
            #print('Flight Leg Record',end=' ')
            #print(legorig,end='-')
            #print(legdest)
            legorig = line[36:39]
            legdest = line[54:57]
            legflight = line[5:9]
            # hub only filter
            if filterhub and not filterdest and not filterflight and not filterorig:
                if (legorig == hub) or (legdest == hub):
                    linecount += 1
                    # line renumbering
                    outline = line[0:194] + str(linecount).zfill(6) + '\n'
                    print(outline)
                    outfile.write(outline)                
            # origin only filter                    
            if filterorig and not filterdest and not filterflight:
                if legorig in origins:
                    linecount += 1
                    # line renumbering
                    outline = line[0:194] + str(linecount).zfill(6) + '\n'
                    print(outline)
                    outfile.write(outline)
            # destination only filter
            if not filterorig and filterdest and not filterflight:
                if legdest in destinations:
                    linecount += 1
                    # line renumbering
                    outline = line[0:194] + str(linecount).zfill(6) + '\n'
                    print(outline)
                    outfile.write(outline)
            # flight only filter
            if not filterorig and not filterdest and filterflight:
                if legflight in flights:
                    linecount += 1
                    # line renumbering
                    outline = line[0:194] + str(linecount).zfill(6) + '\n'
                    print(outline)
                    outfile.write(outline)                    
            # origin & destination filter
            if filterorig and filterdest and not filterflight:
                if (legorig in origins) and (legdest in destinations):
                    linecount += 1
                    # line renumbering
                    outline = line[0:194] + str(linecount).zfill(6) + '\n'
                    print(outline)
                    outfile.write(outline)
            # origin & flight filter
            if filterorig and not filterdest and filterflight:
                if (legorig in origins) and (legflight in flights):
                    linecount += 1
                    # line renumbering
                    outline = line[0:194] + str(linecount).zfill(6) + '\n'
                    print(outline)
                    outfile.write(outline)
            # destination & flight filter
            if not filterorig and filterdest and filterflight:
                if (legdest in destinations) and (legflight in flights):
                    linecount += 1
                    # line renumbering
                    outline = line[0:194] + str(linecount).zfill(6) + '\n'
                    print(outline)
                    outfile.write(outline)
            
        # Record Type 5 > we copy as is to output file                    
        if line[0] == '5':
            print('Trailer Record')
            # line renumbering
            outline = line[0:187] + str(linecount).zfill(6) + 'E' + str(linecount+1).zfill(6) + '\n'
            outfile.write(outline)
            linecount += 1
            
    outfile.close()
    infile.close()