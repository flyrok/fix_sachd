'''
Fix sac headers

'''

# standard system stuff
from pathlib import Path
import logging
import sys

# matplot lib stuff

import numpy as np
from obspy import UTCDateTime, Stream, read
from obspy.signal.filter import envelope
# mine
#from hypoarc.hypoarc import hypoarc, Hpck

#import warnings
#warnings.filterwarnings("ignore") # this is to stop numpy depracate warning


class fix_sachd(object):
    def __init__(self, list_sacs=None,head_dict=None,debug=0,logfile=None):
        '''
        list: list_sacs
            list of paths to sac files to use
        dict: head_dict
            dict of sac header key value pairs. 
        int: debug
            debug level
        str:
            log file name
        '''

        # setup logging
        self.debug=debug
        self.log=self.setup_log(logfile,self.debug)
        # class default inputs
        self.list_sacs=list_sacs
        self.hd=head_dict

        # some variables
        self.st=Stream()

    def run(self):
        # read the sac files from file list 
        self.read_sacfiles(self.list_sacs) 

        # fix headers
        self.fix_head()

        # write output
        self.write_sac()

    def read_sacfiles(self,list_sacs):
        _name=f"{__name__}.read_sacfiles"
        '''
        read in all sac files, 
        ignoring if they have a pick time or not
        '''

        for i in list_sacs:
            if not Path(i).is_file():
                self.log.warn(f'{_name} Problem with {i}, skipping')
                continue
            try:
                tr=read(i,type='SAC')
                tr[0].stats['outfile']=i
                self.st+=tr[0]
            except Exception as e:
                self.log.error(f'{_name} Problem reading {i} ... \n{e}')
                pass
        self.log.debug(f'{_name} Read {len(self.st)} sac files')
        return

    def fix_head(self):
        _name=f"{__name__}.fix_head"
        if not isinstance(self.hd,(dict)):
            self.log.error(f'{_name} not a dict')
            sys.exit(0)
        for key in self.hd.keys():
            for tr in self.st:
                id=tr.id
                self.log.debug(f'{_name} Setting {key} to {self.hd[key]} for {id}')
                tr.stats.sac[key]=self.hd[key]

    def write_sac(self):
        _name=f'{__name__}.rms'
        for tr in self.st:
            try:
                outfile=tr.stats.outfile
                tr.write(outfile,format='SAC')
            except Exception as e:
                self.log.error(f'{_name} {tr.id} ...\n\t{e}')
                pass
    

    def setup_log(self,logfile,debug):

        ''' Helper function to set up logging
            at the right debug level
        '''
        # INFO,DEBUG,WARN
        if debug == 0:
            loglevel="WARN"
        elif debug == 1:
            loglevel="INFO"
        else:
            loglevel="DEBUG"
        if isinstance(logfile,(logging.RootLogger)):
            log=logfile
            log.setLevel(loglevel)
        else:
            logging.basicConfig(filename=logfile, level=loglevel,
                datefmt="%Y-%j %H:%M:%S", format="%(asctime)s-%(levelname)s %(message)s")
            log=logging.getLogger(__name__)

        #if debug > 1 and not log.manager.loggerDict: # this has logs also dumped to screen if debug turned on
        if debug > 1 : # this has logs also dumped to screen if debug turned on
            ch = logging.StreamHandler()
            log.addHandler(ch)
        print(__name__,' loglevel set to ' , loglevel, log.level)
        return log


