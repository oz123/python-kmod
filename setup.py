# Copyright (C) 2012 Red Hat, Inc.
#                    W. Trevor King <wking@tremily.us>
#
# This file is part of python-kmod.
#
# python-kmod is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 2.1 as published
# by the Free Software Foundation.
#
# python-kmod is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-kmod.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
from distutils.extension import Extension as _Extension
from distutils.command import clean as CleanComm
from distutils.dir_util import remove_tree
from distutils import log
from Cython.Distutils import build_ext as _build_ext

import os as _os
import sys as _sys

class CleanCommand(CleanComm.clean):
    def run(self):
        # remove the build/temp.<plat> directory (unless it's already
        # gone)
        if _os.path.exists(self.build_temp):
            remove_tree(self.build_temp, dry_run=self.dry_run)
        else:
            log.debug("'%s' does not exist -- can't clean it",
                      self.build_temp)

        if self.all:
            # remove build directories
            for directory in (self.build_lib,
                              self.bdist_base,
                              self.build_scripts):
                if _os.path.exists(directory):
                    remove_tree(directory, dry_run=self.dry_run)
                else:
                    log.warn("'%s' does not exist -- can't clean it",
                             directory)

        _os.system("find . -iname *.c | xargs rm -vf")
        _os.system("find . -iname *.pyc | xargs rm -vf")

        # just for the heck of it, try to remove the base build directory:
        # we might have emptied it right now, but if not we don't care
        if not self.dry_run:
            try:
                _os.rmdir(self.build_base)
                log.info("removing '%s'", self.build_base)
            except OSError:
                pass


package_name = 'kmod'

# read version from local kmod/version.py without pulling in
# kmod/__init__.py
_sys.path.insert(0, package_name)
from version import __version__


_this_dir = _os.path.dirname(__file__)

ext_modules = []
for filename in sorted(_os.listdir(package_name)):
    basename,extension = _os.path.splitext(filename)
    if extension == '.pyx':
        ext_modules.append(
            _Extension(
                '{0}.{1}'.format(package_name, basename),
                [_os.path.join(package_name, filename)],
                libraries=['kmod'],
                ))

setup(
    name=package_name,
    version=__version__,
    description='Python binding for kmod',
    packages=[package_name],
    provides=[package_name],
    maintainer="Andy Grover",
    maintainer_email="agrover@redhat.com",
    cmdclass = {'build_ext': _build_ext,
                'clean': CleanCommand},
    ext_modules=ext_modules,
    )
