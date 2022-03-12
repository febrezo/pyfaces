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

import random
import textwrap

import pyfaces.misc.fortunes as fortunes
from pyfaces.misc.colors import emphasis
from pyfaces.misc.colors import error
from pyfaces.misc.colors import success
from pyfaces.misc.colors import title
from pyfaces.misc.colors import warning


LICENSE_URL = "https://www.gnu.org/licenses/agpl-3.0.txt"

logo = """
                      ____         __
                     |  _ \ _   _ / _| __ _  ___ ___  ___
                     | |_) | | | | |_ / _` |/ __/ _ \/ __|
                     |  __/| |_| |  _| (_| | (_|  __/\__ \\
                     |_|    \__, |_|  \__,_|\___\___||___/
                            |___/
"""

header = f"""
{title(logo)}


{f"Coded with {error('♥')} by {success('Félix Brezo')} since {emphasis('2020')}".center(113)}

{f"License: {title('AGPLv3')}".center(94)}


{warning(random.choice(fortunes.messages).center(80))}

"""

welcome = textwrap.dedent(header)


def show_license():
    """Method that prints the license if requested.
    It tries to find the license online and manually download it. This method
    only prints its contents in plain text.
    """
    print("Trying to recover the contents of the license...\n")
    try:
        # Grab the license online and print it.
        text = urllib.urlopen(LICENSE_URL).read()
        print("License retrieved from " + emphasis(LICENSE_URL) + ".")
        raw_input("\n\tPress " + emphasis("<ENTER>") + " to print it.\n")
        print(text)
    except:
        print(warning("The license could not be downloaded and printed."))
