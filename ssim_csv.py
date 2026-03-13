# ssim_csv part of the SSIM_utils
# Copyright 2026 Stefano Sinagra sinager@tarapippo.net

''' Utility will process a SSIM file exporting key data into a CSV file
    for better human reading, exporting in tables etc.
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

parser = argparse.ArgumentParser(description ='Utility to export main schedula data from a SSIM to a CSV file.')

parser.add_argument('inputfile', help='inputfile.ssim')
parser.add_argument('outputfile', help='outputfile.ssim')
parser.add_argument('-c','--credits',help='SSIM utilities - Copyright 2026 Stefano Sinagra released under GPLv3 ')

args = parser.parse_args()
infilename = args.inputfile

with open(infilename) as infile:
    print('Scanning file...')
    outfilename = args.outputfile
    outfile= open(outfilename, 'w')
    header = 'cx,flight,from_date,to_date,frequency,orig,loc_etd,utc_etd,dest,eta,utc_eta,date_diff,service\n'
    outfile.write(header)
    for line in infile:
        # Record Type 3 > filters are applied
        if line[0] == '3':
            cxorig = line[2:4]
            fltorig = line[5:9]
            from_date = line[14:21]
            to_date = line[21:28]
            freq =  line[28:35]
            fltfrm = line[36:39]
            loc_etd = line[39:43]
            utc_etd = line[43:52]
            dest = line[54:57]
            loc_eta = line[57:61]
            utc_eta = line[61:70]            
            date_diff = line[192:194]
            service = line[72:77]
            line = cxorig + "," + fltorig + "," + from_date + "," + to_date + "," + freq + "," + fltfrm + "," + loc_etd + "," + utc_etd + "," + dest + "," + loc_eta + "," + utc_eta + "," + date_diff + "," + service + "\n"
            outfile.write(line)
                        
    outfile.close()
    infile.close()

    
