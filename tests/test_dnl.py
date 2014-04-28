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
import support
import unittest


class DnlCommandTest(unittest.TestCase):

    def setUp(self):
        def stub_fn(pkg_spec):
            if '.src.rpm' in pkg_spec:
                return support.Query.filter(sourcerpm=pkg_spec)
            else:
                q = support.Query.latest()
                return [pkg for pkg in q if pkg_spec == pkg.name]
        cli = mock.MagicMock()
        self.cmd = dnl.DnlCommand(cli)
        self.cmd.cli.base.repos = dnf.repodict.RepoDict()
        self.cmd._get_query = stub_fn
        self.cmd._get_query_source = stub_fn
        self.cmd.opts = mock.Mock()
        self.cmd.opts.resolve = False
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

    def tearDown(self):
        del self.cmd

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

    def test_get_source_packages(self):
        print()
        pkg = support.PkgStub('foo', '0', '1.0', '1', 'noarch', 'test-repo')
        found = self.cmd._get_source_packages([pkg])
        self.assertEqual(found[0], 'foo-1.0-1.src.rpm')

    def test_get_query(self):
        print()
        found = self.cmd._get_query('foo')
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, 'foo')
        found = self.cmd._get_query('bar')
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, 'bar')

    def test_get_query_source(self):
        print()
        pkgs = self.cmd._get_query_source('foo-2.0-1.src.rpm')
        self.assertEqual(len(pkgs), 1)
        self.assertEqual(pkgs[0].arch, 'src')
        self.assertEqual(pkgs[0].reponame, 'test-repo-source')

    def test_get_packages(self):
        print()
        pkgs = self.cmd._get_packages(['bar'])
        self.assertEqual(len(pkgs), 1)
        self.assertEqual(pkgs[0].name, 'bar')
        pkgs = self.cmd._get_packages(['bar', 'foo'])
        self.assertEqual(len(pkgs), 2)
        self.assertEqual(pkgs[0].name, 'bar')
        self.assertEqual(pkgs[1].name, 'foo')
        pkgs = self.cmd._get_packages(['notfound'])
        self.assertEqual(len(pkgs), 0)
        pkgs = self.cmd._get_packages(['notfound', 'bar'])
        self.assertEqual(len(pkgs), 1)
        self.assertEqual(pkgs[0].name, 'bar')
        pkgs = self.cmd._get_packages(['foo-2.0-1.src.rpm'], source=True)
        self.assertEqual(len(pkgs), 1)
        self.assertEqual(pkgs[0].arch, 'src')
        self.assertEqual(pkgs[0].reponame, 'test-repo-source')

    def test_download_rpms(self):
        print()
        locations = self.cmd._download_rpms(['foo'])
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], '/tmp/dnf/foo-2.0-1.noarch.rpm')
        locations = self.cmd._download_rpms(['foo', 'bar'])
        self.assertEqual(len(locations), 2)
        self.assertEqual(locations[0], '/tmp/dnf/bar-2.0-1.noarch.rpm')
        self.assertEqual(locations[1], '/tmp/dnf/foo-2.0-1.noarch.rpm')
        self.assertTrue(self.cmd.base.download_packages.called)

    def test_download_source(self):
        print()
        locations = self.cmd. _download_source(['foo'])
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], '/tmp/dnf/foo-2.0-1.src.rpm')
        locations = self.cmd. _download_source(['foo', 'bar'])
        self.assertEqual(len(locations), 2)
        self.assertEqual(locations[0], '/tmp/dnf/bar-2.0-1.src.rpm')
        self.assertEqual(locations[1], '/tmp/dnf/foo-2.0-1.src.rpm')
