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

from __future__ import print_function

import support
import unittest


class SupportTest(unittest.TestCase):

    def test_repostub(self):
        repo = support.RepoStub('test-repo')
        self.assertEqual(repo.id, 'test-repo')
        self.assertFalse(repo.enabled)
        self.assertIsNone(repo.valid())
        repo.enable()
        self.assertTrue(repo.enabled)
        repo.disable()
        self.assertFalse(repo.enabled)

    def test_pkgstub(self):
        print()
        # test package without epoch
        pkg = support.PkgStub('foo', '0', '1.0', '1', 'noarch', 'test-repo')
        self.assertEqual(pkg.name, 'foo')
        self.assertEqual(pkg.epoch, '0')
        self.assertEqual(pkg.version, '1.0')
        self.assertEqual(pkg.release, '1')
        self.assertEqual(pkg.reponame, 'test-repo')
        self.assertEqual(pkg.evr, '1.0-1')
        self.assertEqual(str(pkg), 'foo-1.0-1.noarch : (test-repo)')
        # test package with epoch
        pkg = support.PkgStub('bar', '5', '1.0', '1', 'noarch', 'test-repo')
        self.assertEqual(pkg.evr, '5:1.0-1')
        self.assertEqual(str(pkg), 'bar-5:1.0-1.noarch : (test-repo)')
        self.assertEqual(pkg.sourcerpm, 'bar-5:1.0-1.src.rpm')
        self.assertEqual(pkg.localPkg(), '/tmp/dnf/bar-5:1.0-1.noarch.rpm')
        # test src package
        pkg = support.PkgStub('bar', '5', '1.0', '1', 'src', 'test-repo-source')
        self.assertEqual(pkg.fullname, 'bar-5:1.0-1.src')
        self.assertEqual(pkg.sourcerpm, 'bar-5:1.0-1.src.rpm')
        self.assertEqual(pkg.localPkg(), '/tmp/dnf/bar-5:1.0-1.src.rpm')

    def test_query(self):
        print()
        q = support.Query
        inst = q.installed()
        self.assertEqual(inst, support.PACKAGES_INST)
        avail = q.available()
        self.assertEqual(avail, support.PACKAGES_AVAIL)
        latest = q.latest()
        self.assertEqual(latest, support.PACKAGES_LASTEST)
        found = q.filter(name='foo')
        for pkg in found:
            self.assertEqual(pkg.name, 'foo')
        found = q.filter(sourcerpm='foo-2.0-1.src.rpm')
        for pkg in found:
            self.assertEqual(pkg.fullname, 'foo-2.0-1.src')
            self.assertEqual(pkg.sourcerpm, 'foo-2.0-1.src.rpm')
