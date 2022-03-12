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

import os
import unittest

from pyfaces.core.processor import FaceProcessor


class TestFaceProcessor(unittest.TestCase):
    # Setting up the invironment
    # --------------------------

    def setUp(self):
        """Instantiation of a MooringDispatcher Generic API
        """
        self.proc = FaceProcessor()

    # Proof obtention tests
    # ---------------------
    def test_face_single_extraction(self):
        """Test the face single detection"""
        result = self.proc.extract_faces("./res/hoodie.jpeg")
        
        self.assertEqual(
            len(result),
            1
        )

    def test_face_multiple_extraction(self):
        """Test the face multiple detection"""
        result = self.proc.extract_faces("./res/two_people.jpg")
        
        self.assertEqual(
            len(result),
            3               # Yes, Batman is there
        )

    def test_face_hashing(self):
        """Test the face hashing"""
        result = self.proc.extract_faces("./res/hoodie.jpeg")
        
        self.assertEqual(
            os.path.basename(result[0]),
            "101ed2b1a1e882f2f2512eee9937c1ad.bmp"
        )

if __name__ == '__main__':
    unittest.main()
