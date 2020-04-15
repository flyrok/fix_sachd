#!/usr/bin/env python3

import argparse
from pathlib import Path
from datetime import datetime
import sys
from fix_sachd import fix_sachd

here = Path(__file__).resolve().parent
exec(open(here / "version.py").read())

def main():
    '''
    Fix sac header value
    '''

    parser = argparse.ArgumentParser(prog=progname,
            formatter_class=CustomFormatter,
            description= '''
            fix sac header values
            ''',
            epilog=""""
            e.g.
            sac_codadur -f sac_data/*.sac 
            """
            )

    parser.add_argument("-f","--infiles", type=str,nargs='*',default=None,
        required=True, help="sac files to fix header values")

    parser.add_argument("-d","--hd_dict", type=str,nargs='*',default=None,
        required=True, help="Header value key:value pairs. (e.g. norid:4026")

    parser.add_argument("-l","--logfile", type=str,default=datetime.now().strftime("%Y%j") + ".fix_sachd.log",
        required=False, help="log file name")

    parser.add_argument("-v", "--verbose", action="count",default=0,
        help="increase debug spewage spewage (e.g. -v, -vv, -vvv)")

    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))

    args = parser.parse_args()

    debug = args.verbose
    infiles=args.infiles
    hd_dict=args.hd_dict
    logfile=args.logfile    # logfile name

    # convert hd_dict into dict
    tmp=[j for i in hd_dict for j in i.split(':')]
    hd_dict=dict(zip(tmp[::2],tmp[1::2]))
    # initialize the sac2hypoarc class
    obj=fix_sachd(list_sacs=infiles,head_dict=hd_dict,debug=debug,logfile=logfile)
    # process sac files and save output
    obj.run()


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    '''
    re-class ArgDefaults formatter to also print things pretty. Helps printing out the config file example
    '''
    def _get_help_string(self, action):
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    if type(action.default) == type(sys.stdin):
                        print( action.default.name)
                        help += ' (default: ' + str(action.default.name) + ')'
                    else:
                        help += ' (default: %(default)s)'
        return help

if __name__ == '__main__':
    main()

