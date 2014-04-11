#    dnf-utils - add-on tools for DNF
#    Copyright (C) 2014 Tim Lauridsen < timlau<AT>fedoraproject<DOT>org >
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import sys
sys.path[0] = '/home/tim/udv/work/dnf-utils/'

from dnfutils import logger, _, ArgumentParser

import dnf
import dnf.cli
import dnf.exceptions


class Sample(dnf.Plugin):

    name = 'sample'

    def __init__(self, base, cli):
        self.base = base
        self.cli = cli
        logger.debug('init sample plugin')
        if self.cli is not None:
            self.cli.register_command(SampleCommand)


class SampleCommand(dnf.cli.Command):
    """ the util command there is extending the dnf command line """

    aliases = ['sample-util']
    # summary for util, shown in dnf help
    summary = _('One line description of the util')
    # usage string for the util
    usage = _('[PARAMETERS]')

    def configure(self, args):
        ''' do the util config here '''
        pass

    def run(self, args):
        ''' execute the util action here '''
        logger.debug('Command sample : run')
        parser = ArgumentParser(prog='dnf sample-util')
        parser.add_argument("cmd", nargs=1, help='the sub command')
        parser.add_argument("parms", nargs='*',
                            help='the parameters to the sub command')
        parser.add_argument("--some-option", action='store_true',
                            help='an optional option')
        try:
            opts = parser.parse_args(args)
        except AttributeError as e:
            print(parser.format_help())
            raise dnf.exceptions.Error(str(e))

        print('Sample util is running with :')
        print('    cmd =       : %s' % opts.cmd)
        print('    parms =     : %s' % opts.parms)
        print('    some-option : %s' % opts.some_option)

        return 0, ''
