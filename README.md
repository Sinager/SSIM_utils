# SSIM_utils
Scripts to perform simple operations on IATA SSIM schedule files
https://en.wikipedia.org/wiki/Standard_Schedules_Information_Manual

ssim_remap

Utility will rename flight numbers into a SSIM file according to a map stored into a csv file.
Example entry in mapping file: XX0123,YY0789
Flight XX0123 will be changed into flight YY0789
Original operating period can be overwritten to new dates.
You can choose whether to keep in output file non remapped flights.

ssim_csv

Will process a SSIM file exporting key data into a CSV file for better human reading, exporting in tables etc.

ssim_filter

Utility will process a SSIM file filtering only services we are interested in.
User can filter by origins, destinations, hub, flight numbers.

Usage is via command line and a Python interpeter must be installed on your pc.
Example:
python ssim_csv -h
will print some usage instructions
