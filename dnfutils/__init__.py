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

""" Common code for dnf-utils"""
from __future__ import print_function

from gettext import NullTranslations
from sys import version_info

import argparse
import dnf.exceptions
import gettext
import logging

# lint:disable
# python 3 compabillity settings
if version_info.major >= 3:
    PY3 = True
    basestring = unicode = str  # @UnusedVariable
    # u?gettext dont exists in python3 NullTranslations
    NullTranslations.ugettext = NullTranslations.gettext
    NullTranslations.ungettext = NullTranslations.ngettext
else:
    from __builtin__ import unicode, basestring  # @UnresolvedImport
    PY3 = False

# lint:enable

t = gettext.translation('dnf-utils', fallback=True)
_ = t.ugettext
P_ = t.ungettext

logger = logging.getLogger('dnf.dnf-utils')


class ArgumentParser(argparse.ArgumentParser):
    """ Argument parser for dnf-utils

    help commands (-h, --help) is disabled by default

    Use it to parse parameter send to the util cmd from DNF.
    """

    def __init__(self, cmd, **kwargs):
        argparse.ArgumentParser.__init__(self, prog="dnf {}".format(cmd),
                                         add_help=False, **kwargs)
        self.add_argument("--help-cmd", action='store_true',
                          help=_('show this help about this tool'))

    def error(self, message):
        ''' overload the default error method

        We dont wan't the default exit action on parse
        errors, just raise an AttributeError, the util can
        catch
        '''
        raise AttributeError(message)

    def parse_args(self, args):
        try:
            opts = argparse.ArgumentParser.parse_args(self, args)
        except AttributeError as e:
            print(self.format_help())
            raise dnf.exceptions.Error(str(e))
        return opts
