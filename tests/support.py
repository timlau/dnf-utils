# Copyright (C) 2014  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

import dnf
import logging
import sys

PY3 = False
if sys.version_info.major >= 3:
    PY3 = True

if PY3:
    from unittest import mock
else:
    import mock


class BaseCliStub(object):
    """A class mocking `dnf.cli.cli.BaseCli`."""

    def __init__(self, available_pkgs=(), available_groups=()):
        """Initialize the base."""
        self._available_pkgs = set(available_pkgs)
        self._available_groups = set(available_groups)
        self.installed_groups = set()
        self.installed_pkgs = set()
        self.repos = dnf.repodict.RepoDict()

    def install_grouplist(self, names):
        """Install given groups."""
        to_install = (set(names) & self._available_groups) - self.installed_groups
        if not to_install:
            raise dnf.exceptions.Error('nothing to do')
        self.installed_groups.update(to_install)

    def install(self, pattern):
        """Install given package."""
        if pattern not in self._available_pkgs or pattern in self.installed_pkgs:
            raise dnf.exceptions.MarkingError('no package matched')
        self.installed_pkgs.add(pattern)

    def read_all_repos(self):
        """Read repositories information."""
        self.repos.add(RepoStub('main'))

    def read_comps(self):
        """Read groups information."""
        if not self._available_groups:
            raise dnf.exceptions.CompsError('no group available')


class CliStub(object):
    """A class mocking `dnf.cli.Cli`."""

    nogpgcheck = True

    def __init__(self, base):
        """Initialize the CLI."""
        self.base = base
        self.cli_commands = {}
        self.logger = logging.getLogger()
        self.register_command(dnf.cli.commands.HelpCommand)

    def register_command(self, command):
        """Register given *command*."""
        self.cli_commands.update({alias: command for alias in command.aliases})


class RepoStub(object):
    """A class mocking `dnf.repo.Repo`"""

    enabled = False

    def __init__(self, id_):
        """Initialize the repository."""
        self.id = id_

    def valid(self):
        """Return a message if the repository is not valid."""

    def enable(self):
        """ Enable the repo"""
        self.enabled = True

    def disable(self):
        """ Disable the repo"""
        self.enabled = False


class PkgStub:
    def __init__(self, n, e, v, r, a, repo_id):
        """ mocking dnf.package.Package"""
        self.name = n
        self.version = v
        self.release = r
        self.arch = a
        self.epoch = e
        self.reponame = repo_id

    def __str__(self):
        return "{0.name}-{0.evr}.{0.arch} : ({0.reponame})".format(self)

    @property
    def evr(self):
        if self.epoch != '0':
            return "{0.epoch}:{0.version}-{0.release}".format(self)
        else:
            return "{0.version}-{0.release}".format(self)

    @property
    def sourcerpm(self):
        if self.arch != 'src':
            return "{0.name}-{0.evr}.src.rpm".format(self)
        else:
            return "{0.name}-{0.evr}.{0.arch}.rpm".format(self)

    @property
    def fullname(self):
        return "{0.name}-{0.evr}.{0.arch}".format(self)

    def localPkg(self):
        return "/tmp/dnf/{0.name}-{0.evr}.{0.arch}.rpm".format(self)


class QueryStub(object):
    """ mocking dnf'.sack.Sack'"""
    def __init__(self, inst, avail, latest, sources):
        self._inst = inst
        self._avail = avail
        self._latest = latest
        self._sources = sources
        self._all = []
        self._all.extend(inst)
        self._all.extend(avail)

    def available(self):
        return self.filter(available=True)

    def installed(self):
        return self.filter(installed=True)

    def latest(self):
        return self.filter(latest=True)

    def filter(self, **kwargs):
        if 'available' in kwargs:
            return self._avail
        elif 'installed' in kwargs:
            return self._inst
        elif 'latest' in kwargs:
            return self._latest
        elif 'name' in kwargs:
            name = kwargs['name']
            return [pkg for pkg in self._all if pkg.name == name]
        elif 'sourcerpm' in kwargs:
            src_name = kwargs['sourcerpm']
            return [pkg for pkg in self._sources if pkg.sourcerpm == src_name]


PACKAGES_AVAIL = [
PkgStub('foo', '0', '1.0', '1', 'noarch', 'test-repo'),
PkgStub('foo', '0', '2.0', '1', 'noarch', 'test-repo'),
PkgStub('bar', '0', '1.0', '1', 'noarch', 'test-repo'),
PkgStub('bar', '0', '2.0', '1', 'noarch', 'test-repo'),
PkgStub('foobar', '0', '1.0', '1', 'noarch', 'test-repo'),
PkgStub('foobar', '0', '2.0', '1', 'noarch', 'test-repo')
]

PACKAGES_LASTEST = [
PACKAGES_AVAIL[1],
PACKAGES_AVAIL[3],
PACKAGES_AVAIL[5]
]

PACKAGES_INST = [
PkgStub('foo', '0', '1.0', '1', 'noarch', '@System'),
PkgStub('foobar', '0', '1.0', '1', 'noarch', '@System')
]

PACKAGES_SOURCE = [
PkgStub('foo', '0', '1.0', '1', 'src', 'test-repo-source'),
PkgStub('foo', '0', '2.0', '1', 'src', 'test-repo-source'),
PkgStub('bar', '0', '1.0', '1', 'src', 'test-repo-source'),
PkgStub('bar', '0', '2.0', '1', 'src', 'test-repo-source'),
PkgStub('foobar', '0', '1.0', '1', 'src', 'test-repo-source'),
PkgStub('foobar', '0', '2.0', '1', 'src', 'test-repo-source')
]

Query = QueryStub(PACKAGES_INST, PACKAGES_AVAIL,
                  PACKAGES_LASTEST, PACKAGES_SOURCE)
