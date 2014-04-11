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

import argparse
import gettext
import logging

t = gettext.translation('dnf-utils', fallback=True)
_ = t.ugettext
P_ = t.ungettext

logger = logging.getLogger('dnf.dnf-utils')


class ArgumentParser(argparse.ArgumentParser):
    """ Argument parser for dnf-utils

    help commands (-h, --help) is disabled by default

    Use it to parse parameter send to the util cmd from DNF.
    """

    def __init__(self, **kwargs):
        argparse.ArgumentParser.__init__(self, add_help=False, **kwargs)

    def error(self, message):
        ''' overload the default error method

        We dont wan't the default exit action on parse
        errors, just raise an AttributeError, the util can
        catch
        '''
        raise AttributeError(message)
