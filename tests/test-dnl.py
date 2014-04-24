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

from support import mock, RepoStub

import dnf.repodict
import dnl
import unittest


class DnlCommandTest(unittest.TestCase):

    def setUp(self):
        cli = mock.MagicMock()
        self.cmd = dnl.DnlCommand(cli)
        self.cmd.cli.base.repos = dnf.repodict.RepoDict()
        repo = RepoStub('foo')
        repo.enable()
        self.cmd.base.repos.add(repo)
        repo = RepoStub('foo-source')
        repo.disable()
        self.cmd.base.repos.add(repo)
        repo = RepoStub('bar')
        repo.enable()
        self.cmd.base.repos.add(repo)
        repo = RepoStub('foobar-source')
        repo.disable()
        self.cmd.base.repos.add(repo)

    def test_enable_source_repos(self):
        print()
        repos = self.cmd.base.repos
        self.assertTrue(repos['foo'].enabled)
        self.assertFalse(repos['foo-source'].enabled)
        self.assertTrue(repos['bar'].enabled)
        self.assertFalse(repos['foobar-source'].enabled)
        self.cmd._enable_source_repos()
        self.assertTrue(repos['foo-source'].enabled)
        self.assertFalse(repos['foo'].enabled)
        self.assertFalse(repos['bar'].enabled)
        self.assertFalse(repos['foobar-source'].enabled)
        print(self.cmd.base.fill_sack.called)


