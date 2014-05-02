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

from datetime import datetime
from dnfutils import logger, _

import dnf
import dnf.cli
import dnf.exceptions
import dnfutils
import functools
import hawkey
import re

# march a %[-][dd]{attr}
QF_MATCH = re.compile(r'%([-\d]*?){([:\.\w]*?)}')

QUERY_TAGS = """
name, arch, epoch, version, release, reponame (repoid), evr
installtime, buildtime, size, downloadsize, installize
provides, requires, obsoletes, conflicts, sourcerpm
description, summary, license, url
"""


class Query(dnf.Plugin):

    name = 'Query'

    def __init__(self, base, cli):
        self.base = base
        self.cli = cli
        logger.debug('Initialized %s plugin', self.name)
        if self.cli is not None:
            self.cli.register_command(QueryCommand)


class QueryCommand(dnf.cli.Command):
    """ the util command there is extending the dnf command line """
    aliases = ['query']
    # summary for util, shown in dnf help
    summary = _('search for packages matching keyword')
    # usage string for the util
    usage = _('[OPTIONS] [KEYWORDS]')

    def get_format(self, qf):
        """ convert a rpm like QUERYFMT to an python .format() string """
        def fmt_repl(matchobj):
            fill = matchobj.groups()[0]
            key = matchobj.groups()[1]
            if fill:
                if fill[0] == '-':
                    fill = '>' + fill[1:]
                else:
                    fill = '<' + fill
                fill = ':' + fill
            return '{0.' + key.lower() + fill + "}"

        if not qf:
            qf = '%{name}-%{epoch}:%{version}-%{release}.%{arch} : %{reponame}'
        qf = qf.replace("\\n", "\n")
        qf = qf.replace("\\t", "\t")
        fmt = re.sub(QF_MATCH, fmt_repl, qf)
        return fmt

    def show_packages(self, query, fmt):
        for po in query.run():
            try:
                pkg = PackageWrapper(po)
                print(fmt.format(pkg))
            except AttributeError as e:
                # catch that the user has specified attributes
                # there don't exist on the dnf Package object.
                raise dnf.exceptions.Error(str(e))

    def configure(self, args):
        demands = self.cli.demands
        demands.sack_activation = True
        demands.available_repos = True

    def run(self, args):
        """ execute the util action here """
        # Setup ArgumentParser to handle util
        parser = dnfutils.ArgumentParser(self.aliases[0])
        parser.add_argument('key', nargs='?',
                            help=_('the key to search for'))
        parser.add_argument('--all', action='store_true',
                            help=_('query in all packages (Default)'))
        parser.add_argument('--installed', action='store_true',
                            help=_('query in installed packages'))
        parser.add_argument('--latest', action='store_true',
                            help=_('show only latest packages'))
        parser.add_argument('--qf', "--queryformat", dest='queryformat',
                            help=_('format for displaying found packages'))
        parser.add_argument('--repoid', metavar='REPO',
                            help=_('show only results from this REPO'))
        parser.add_argument('--arch', metavar='ARCH',
                            help=_('show only results from this ARCH'))
        parser.add_argument('--whatprovides', metavar='REQ',
                            help=_('show only results there provides REQ'))
        parser.add_argument('--whatrequires', metavar='REQ',
                            help=_('show only results there requires REQ'))
        parser.add_argument('--showtags', action='store_true',
                            help=_('show available tags to use with '
                                   '--queryformat'))
        logger.debug('Command sample : run')
        opts = parser.parse_args(args)

        if opts.help_cmd:
            print(parser.format_help())
            return

        if opts.showtags:
            print(_('Available query-tags: use --queryformat ".. %{tag} .."'))
            print(QUERY_TAGS)
            return

        q = self.base.sack.query()
        if opts.all:
            q = q.available()
        elif opts.installed:
            q = q.installed()
        if opts.latest:
            q = q.latest()
        if opts.key:
            if set(opts.key) & set('*[?'):  # is pattern ?
                fdict = {'name__glob': opts.key}
            else:  # substring
                fdict = {'name__substr': opts.key}
            q = q.filter(hawkey.ICASE, **fdict)
        if opts.repoid:
            q = q.filter(reponame=opts.repoid)
        if opts.arch:
            q = q.filter(arch=opts.arch)
        if opts.whatprovides:
            q = self.by_provides(self.base.sack, [opts.whatprovides], q)
        if opts.whatrequires:
            q = self.by_requires(self.base.sack, opts.whatrequires, q)
        fmt = self.get_format(opts.queryformat)
        self.show_packages(q, fmt)

    def by_provides(self, sack, pattern, query):
        try:
            reldeps = list(map(functools.partial(hawkey.Reldep, sack),
                               pattern))
        except hawkey.ValueException:
            return query.filter(empty=True)
        return query.filter(provides=reldeps)

    def by_requires(self, sack, pattern, query):
        try:
            reldep = hawkey.Reldep(sack, pattern)
        except hawkey.ValueException:
            return query.filter(empty=True)
        return query.filter(requires=reldep)


class PackageWrapper(object):

    def __init__(self, pkg):
        self._pkg = pkg

    def __getattr__(self, attr):
        if hasattr(self._pkg, attr):
            return getattr(self._pkg, attr)
        else:
            raise AttributeError

###############################################################################
# Overloaded attributes there need output formatting
###############################################################################

    @property
    def obsoletes(self):
        return self._reldep_to_list(self._pkg.obsoletes)

    @property
    def conflicts(self):
        return self._reldep_to_list(self._pkg.obsoletes)

    @property
    def requires(self):
        return self._reldep_to_list(self._pkg.requires)

    @property
    def provides(self):
        return self._reldep_to_list(self._pkg.provides)

    @property
    def installtime(self):
        return self._get_timestamp(self._pkg.installtime)

    @property
    def buildtime(self):
        return self._get_timestamp(self._pkg.buildtime)

###############################################################################
# Helpers
###############################################################################

    def _get_timestamp(self, timestamp):
        if timestamp > 0:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M")
        else:
            return ''

    def _reldep_to_list(self, obj):
        return ', '.join([str(reldep) for reldep in obj])
