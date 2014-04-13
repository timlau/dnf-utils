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
from dnfutils import logger, _, ArgumentParser

import dnf
import dnf.cli
import dnf.exceptions
import hawkey


class Query(dnf.Plugin):

    name = 'Query'

    def __init__(self, base, cli):
        self.base = base
        self.cli = cli
        logger.debug('Initialized %s plugin' % self.name)
        if self.cli is not None:
            self.cli.register_command(QueryCommand)


class QueryCommand(dnf.cli.Command):
    """ the util command there is extending the dnf command line """
    aliases = ['query']
    activate_sack = True

    # summary for util, shown in dnf help
    summary = _('search for packages matching keyword')
    # usage string for the util
    usage = _('[OPTIONS] [KEYWORDS]')

    def show_packages(self, query):
        for pkg in query.run():
            print(pkg)

    def run(self, args):
        ''' execute the util action here '''
        # Setup ArgumentParser to handle util
        self.parser = ArgumentParser(prog='dnf query')
        self.parser.add_argument("key", nargs=1,
                            help='the key to search for')
        self.parser.add_argument("--all", action='store_true',
                            help='query in all packages')
        self.parser.add_argument("--installed", action='store_true',
                            help='query in all packages')
        self.parser.add_argument("--latest", action='store_true',
                            help='show only latest packages')
        logger.debug('Command sample : run')
        try:
            opts = self.parser.parse_args(args)
        except AttributeError as e:
            print(self.parser.format_help())
            raise dnf.exceptions.Error(str(e))

        q = self.base.sack.query()
        if opts.all:
            q = q.available()
        elif opts.installed:
            q = q.installed()
        fdict = {'name__substr': opts.key}
        q = q.filter(hawkey.ICASE, **fdict)
        if opts.latest:
            q.latest()
        self.show_packages(q)


        return 0, ''
