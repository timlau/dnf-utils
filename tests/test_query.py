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

from support import mock

import unittest
import query


class Pkg:
    def __init__(self):
        self.name = "foobar"
        self.version = '1.0.1'
        self.release = '1.f20'
        self.arch = 'x86_64'
        self.reponame = "@System"


class SampleCommandTest(unittest.TestCase):

    def test_get_format(self):
        cli = mock.Mock()
        cmd = query.QueryCommand(cli)
        fmt = cmd.get_format('%{name}')
        self.assertEqual(fmt, '{0.name}')
        fmt = cmd.get_format('%40{name}')
        self.assertEqual(fmt, '{0.name:<40}')
        fmt = cmd.get_format('%-40{name}')
        self.assertEqual(fmt, '{0.name:>40}')
        fmt = cmd.get_format('%{name}-%{repoid} :: %-40{arch}')
        self.assertEqual(fmt, '{0.name}-{0.repoid} :: {0.arch:>40}')

    def test_output(self):
        cli = mock.Mock()
        cmd = query.QueryCommand(cli)
        pkg = Pkg()
        fmt = cmd.get_format('%{name}')
        self.assertEqual(fmt.format(pkg), 'foobar')
        fmt = cmd.get_format(
            '%{name}-%{version}-%{release}.%{arch} (%{reponame})')
        self.assertEqual(fmt.format(pkg),
            'foobar-1.0.1-1.f20.x86_64 (@System)')

    def test_illegal_attr(self):
        cli = mock.Mock()
        cmd = query.QueryCommand(cli)
        pkg = Pkg()
        with self.assertRaises(AttributeError) as e:
            cmd.get_format('%{notfound}').format(pkg)
            self.assertEqual(str(e),
                "Pkg instance has no attribute 'notfound'")