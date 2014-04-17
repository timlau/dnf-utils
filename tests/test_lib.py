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
from dnfutils import _, P_, basestring
#from support import mock

import dnfutils
import dnf.exceptions
import unittest


class DnfUtilsTest(unittest.TestCase):

    def test_argparse(self):
        ''' Test the ArgumentParser '''
        parser = dnfutils.ArgumentParser('test')
        parser.add_argument("cmd", nargs=1)
        parser.add_argument("parms", nargs='*')
        self.assertEqual(parser.prog, 'dnf test')
        # test --show-help is added
        self.assertIn('--show-help', parser._option_string_actions)
        # test unknown option
        self.assertRaises(dnf.exceptions.Error, parser.parse_args, ['--dummy'])
        # test --show-help is working
        opts = parser.parse_args(['subcmd', '--show-help'])
        self.assertTrue(opts.show_help)
        # test args
        opts = parser.parse_args(['subcmd', 'parm1', 'parm2'])
        self.assertEqual(opts.cmd, ['subcmd'])
        self.assertEqual(opts.parms, ['parm1', 'parm2'])

    def test_translation_wrappers(self):
        ''' Test Translation wrappers'''
        self.assertTrue(isinstance(_('text'), basestring))
        self.assertEqual(_('notfoundxxx'), 'notfoundxxx')
        self.assertTrue(isinstance(P_('text', 'texts', 2), basestring))
        self.assertEqual(P_('notfound01', 'notfound02', 1), 'notfound01')
        self.assertEqual(P_('notfound01', 'notfound02', 2), 'notfound02')
