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
import dnf.subject
import functools
import itertools
import os
import shutil


class Dnl(dnf.Plugin):

    name = 'dnl'

    def __init__(self, base, cli):
        self.base = base
        self.cli = cli
        logger.debug('Initialized %s plugin' % self.name)
        if self.cli is not None:
            self.cli.register_command(DnlCommand)


class DnlCommand(dnf.cli.Command):
    """ the util command there is extending the dnf command line """

    aliases = ['dnl']
    summary = _('download packages from repositories')
    usage = _('PACKAGE..')

    def configure(self, args):
        demands = self.cli.demands
        demands.sack_activation = True
        demands.available_repos = True

    def run(self, args):
        ''' execute the util action here '''
        logger.debug('Command sample : run')
        # Setup ArgumentParser to handle util
        # You must only add options not used by dnf already
        self.parser = ArgumentParser(self.aliases[0])
        self.parser.add_argument("packages", nargs='*',
                            help=_('packages to download'))
        self.parser.add_argument("--source", action='store_true',
                            help=_('download the src.rpm instead'))
        self.parser.add_argument("--destdir",
                            help=_('download path, default is current dir'))

        # parse the options/args
        # list available options/args on errors & exit
        opts = self.parser.parse_args(args)

        # show util help & exit
        if opts.show_help:
            print(self.parser.format_help())
            return 0, ''

        if opts.source:
            locations = self._download_source(opts.packages)
        else:
            locations = self._download_rpms(opts.packages)

        if opts.destdir:
            dest = opts.destdir
        else:
            dest = os.getcwd()

        move = functools.partial(self._move_package, dest)
        map(move, locations)
        return 0, ''

    def _download_rpms(self, pkg_specs):
        """ Download packages to dnf cache """
        pkgs = self._get_packages(pkg_specs)
        self.base.download_packages(pkgs, self.base.output.progress)
        locations = sorted([pkg.localPkg() for pkg in pkgs])
        return locations

    def _download_source(self, pkg_specs):
        """ Download source packages to dnf cache """
        pkgs = self._get_packages(pkg_specs)
        source_pkgs = set()
        for pkg in pkgs:
            source_pkgs.add(pkg.sourcerpm)
            logger.debug("  --> Package {0} Source : {1}".format(str(pkg), pkg.sourcerpm))
        self._enable_source_repos()
        pkgs = self._get_packages(list(source_pkgs))
        print(pkgs)
        self.base.download_packages(pkgs, self.base.output.progress)
        locations = sorted([pkg.localPkg() for pkg in pkgs])
        return locations

    def _get_packages(self, pkg_specs):
        """ get list of packages matching pkg_specs"""
        queries = map(self._latest_available, pkg_specs)
        pkgs = list(itertools.chain(*queries))
        return pkgs

    def _enable_source_repos(self):
        repo_dict = {}
        # find the source repos for the enabled binary repos
        for repo in self.base.repos.iter_enabled():
            source_repo = "{}-source".format(repo.id)
            if source_repo in self.base.repos:
                repo_dict[repo.id] = (repo, self.base.repos[source_repo])
            else:
                repo_dict[repo.id] = (repo, None)
        # disable the binary & enable the source ones
        for id_ in repo_dict:
            repo, src_repo = repo_dict[id_]
            repo.disable()
            if src_repo:
                logger.info(_("enabled {} repository").format(src_repo.id))
                src_repo.enable()
       # reload the sack
        self.base.fill_sack()

    def _latest_available(self, pkg_spec):
        if '.src.rpm' in pkg_spec:
            return self._latest_available_source(pkg_spec)
        else:
            subj = dnf.subject.Subject(pkg_spec)
            q = subj.get_best_query(self.base.sack)
            q = q.available()
            q = q.latest()
            return q

    def _latest_available_source(self, pkg_spec):
        pkg_spec = pkg_spec[:-8]
        n, v, r = pkg_spec.split('-')
        q = self.base.sack.query()
        q = q.available()
        q = q.latest()
        q = q.filter(name=n, version=v, release=r, arch='src')
        return q

    def _move_package(self, target, location):
        shutil.copy(location, target)
        os.unlink(location)
        return target
