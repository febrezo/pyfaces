################################################################################
#
#    Copyright 2020-2022 @ Félix Brezo (@febrezo)
#
#    This program is part of Pyfaces. You can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

from setuptools import find_packages, setup

import pyfaces


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='Pyfaces',
    version=pyfaces.__version__,
    author='Félix Brezo (@febrezo)',
    description='A package to ease face recognition tasks using Dlib',
    url='https://github.com/febrezo/pyfaces',
    license='GNU AGPLv3+',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyfacesd = pyfaces.server:main',
            'pyfaces = pyfaces.cli:main',
        ],
    },
    install_requires=requirements,
)

