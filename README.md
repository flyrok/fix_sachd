## fix_sachd ##

Reset sac header values

### Purpose/Scope ###

To reset the SAC header values, for one or more headers, for a group of file
Header values are enter on the command line as a series of key:value pairs.

Files are over written, so care should be taken

## Install ##

Clone source package  
`git clone http://github.com/flyrok/fix_sachd`

Install with pip after download  
`pip install .`

Install in editable mode  
`pip install -e .`

Or install directly from github  
`pip install git+https://github.com/flyrok/fix_sachd#egg=fix_sachd`


## Python Dependencies ##

python>=3.6 
obspy (https://github.com/obspy/obspy/wiki)
-- without this, nothing will work

## Usage/Examples ##

To see help:  
`fix_sachd --help`    

To see version:  
`fix_sachd --version`  

To reset the norid value for a group of files:  
`fix_sachd -f sac_data/*.sac -d orid:1000`  

To reset the nzhour nzmin for a group of files:  
`fix_sachd -f sac_data/*.sac -d nzhour:10 nzmin:59`  




