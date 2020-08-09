################################################################################
#
#    Copyright 2020 @ Félix Brezo (@febrezo)
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

import base64
import concurrent.futures
import hashlib
import json
import os
import pathlib
from PIL import Image

import face_recognition
import numpy as np

from pyfaces.core.configuration import ConfigManager
from pyfaces.misc.colors import warning


class FaceProcessor:
    """The class professor

    Attributes:
        config (ConfigManager): The configuration manager object.
        encodings (dict): The encodings file as a dict. The key is the file name.
        comparisons (dict): The comparisons file as a dict. The key is the file name.
    """
    def __init__(self):
        self.config = ConfigManager()
        
        # Load previous configurations
        try:
            with open(str(self.config.comparisons_file), "r") as input_file:
                self.comparisons = json.load(input_file)
        except FileNotFoundError:
            with open(self.config.comparisons_file, "w") as output_file:
                json.dump({}, output_file)
                self.comparisons = {}
        
        try:
            with open(self.config.encodings_file, "r") as input_file:
                self.encodings = json.load(input_file)
        except FileNotFoundError:
            with open(self.config.encodings_file, "w") as output_file:
                json.dump({}, output_file)
                self.encodings = {}

    def compare_faces(self, face_path_1, face_path_2, force_recalculation=False):
        """Compare two existing faces

        Args:
            face_path_1 (str): The path to the first face.
            face_path_2 (str): The path to the first face.
            force_recalculation (bool): If True, it recalculates the process.

        Returns:
            float. The similarity between both faces
        """
        if not force_recalculation:
            if face_path_1 in self.comparisons.keys() and face_path_2 in self.comparisons[face_path_1].keys():
                return self.comparisons[face_path_1][face_path_2]

        if face_path_1 not in self.encodings.keys():
            raise ValueError(f"Image '{face_path_1}' is not a registered face. Try extracting faces first.")
        elif face_path_2 not in self.encodings.keys():
            raise ValueError(f"Image '{face_path_2}' is not a registered face. Try extracting faces first.")

        # Calculate distances
        new_numpy = np.array(self.encodings[face_path_2]["encodings"])

        distance = float(
            face_recognition.face_distance(
                self.encodings[face_path_1]["encodings"],    # It SHOULD BE a list of lists
                new_numpy                               # It SHOULD BE a numpy.array
            )
        )

        # Persisting distance
        with open(self.config.comparisons_file, "r") as input_file:
            self.comparisons = json.load(input_file)

        if face_path_1 not in self.comparisons.keys():
            self.comparisons[face_path_1] = {}
        self.comparisons[face_path_1].update(
            {
                face_path_2: distance
            }
        )
        if face_path_2 not in self.comparisons.keys():
            self.comparisons[face_path_2] = {}
        self.comparisons[face_path_2].update(
            {
                face_path_1: distance
            }
        )

        with open(self.config.comparisons_file, "w") as output_file:
            json.dump(self.comparisons, output_file)

        return distance

    def delete_analysis(self, image_path):
        """Extract faces

        Args:
            image_path (str): The path to the image.

        Raises:
            OSError.
            FileNotFoundError.
        """
        # TODO: Add unlink(missing_ok=True) in Python3.8+
        pathlib.Path(image_path).unlink()

        try:
            with open(self.config.encodings_file, "r") as input_file:
                self.encodings = json.load(input_file)
            
            faces_in_image = []
            copy_encodings = dict(self.encodings)
            for (key, value) in copy_encodings.items() :
                if value["original_file"] == image_path:
                    faces_in_image.append(key)
                    del self.encodings[key]
            
            with open(self.config.encodings_file, "w") as output_file:
                json.dump(self.encodings, output_file)            
        except FileNotFoundError:
            with open(self.config.encodings_file, "w") as output_file:
                json.dump({}, output_file)

        try:
            with open(self.config.comparisons_file, "r") as input_file:
                self.comparisons = json.load(input_file)
            
            copy_comparisons = dict(self.comparisons)
            for (key, value) in copy_comparisons.items() :
                for face in faces_in_image:
                    if key == face:
                        del self.comparisons[key]
                    else:
                        self.comparisons[key].pop(face, None)
            
            with open(self.config.comparisons_file, "w") as output_file:
                json.dump(self.comparisons, output_file)
        except FileNotFoundError:
            with open(self.config.comparisons_file, "w") as output_file:
                json.dump({}, output_file)
        return True

    def extract_faces(self, image_path, force_recalculation=False):
        """Extract faces

        Args:
            image_path (str): The path to the image.
            force_recalculation (bool): If True, it recalculates the process.

        Return:
            list. List of face_paths.

        Raises:
            OSError.
        """
        image_array = face_recognition.load_image_file(image_path)
        image = Image.fromarray(image_array)
        full_image_path = os.path.join(
            self.config.sources_folder,
            hashlib.md5(image.tobytes()).hexdigest() + ".bmp"
        )

        # If the original image is found, it's assumed that the analysis has been performed
        if os.path.exists(full_image_path) and not force_recalculation:
            results = []
            for face in self.encodings.keys():
                if self.encodings[face]["copied_file"] == full_image_path:
                    results.append(face)
            return results

        # Extract faces
        max_width, max_height = image.size
        face_locations = face_recognition.face_locations(image_array)

        new_faces_paths = []

        for i, f in enumerate(face_locations):
            # Cutting out the face
            top, right, bottom, left = f
            face_image_array = image_array[
                max(top-40, 0):min(bottom+20, max_height),
                max(left-15, 0):min(right+15, max_width)
            ]
            pil_image = Image.fromarray(face_image_array)

            full_face_path = os.path.join(
                self.config.faces_folder,
                hashlib.md5(pil_image.tobytes()).hexdigest() + ".bmp"
            )

            pil_image.save(full_face_path)

            # Extract the encodings and saving them
            known_image = face_recognition.load_image_file(full_face_path)
            known_encodings = face_recognition.face_encodings(known_image)

            # Deal with Array object by converting to list. Rememeber to undo this!
            l = []
            for a in known_encodings:
                l.append(a.tolist())
            
            if l != []:
                aux_encoding = {
                    full_face_path: {
                        "original_file": image_path,
                        "copied_file": full_image_path,
                        "encodings": l
                    }
                }

                try:
                    with open(self.config.encodings_file, "r") as input_file:
                        self.encodings = json.load(input_file)
                    self.encodings.update(aux_encoding)
                    with open(self.config.encodings_file, "w") as output_file:
                        json.dump(self.encodings, output_file)
                except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
                    with open(self.config.encodings_file, "w") as output_file:
                        json.dump(aux_encoding, output_file)

                new_faces_paths.append(full_face_path)
            else:
                pathlib.Path(full_face_path).unlink()
            
        # Save the source image
        image.save(full_image_path)
        return new_faces_paths

    def get_face(self, face_path):
        """Get the details of a face

        Args:
            face_path (str): The face path which will be used as a key.

        Returns:
            dict. A dictionary containing the encoding information.

        Raises:
            Exception.
            FileNotFoundException.
        """
        try:
            return self.encodings["face_path"]
        except KeyError:
            raise Exception(f"No encodings found for: '{face_path}'")

    def get_image(self, image_path):
        """Get the base64 encoded image

        Args:
            image_path (str): The image path.

        Returns:
            str. The base64 encoded image.

        Raises:
            Exception.
            FileNotFoundException.
        """
        with open(image_path, "rb") as image_file:
            data = image_file.read()
            return base64.b64encode(data)

        try:
            return self.encodings["face_path"]
        except KeyError:
            raise Exception(f"No encodings found for: '{face_path}'")

    def guess_face(self, new_face_path, force_recalculation=False):
        """Find the most appropiate match.

        This function starts a Task

        Args:
            new_face_path (str): The file path of the task to edal with.
            force_recalculation (bool): If True, it recalculates the process.

        Returns:
            dict. Containing the task details:
            {
                "total_comparisons": …,
                "results": [
                    …
                ]
            }
            
        Raises:
            Exception.
            ValueError.
        """
        # Check if the path provided already has an encoding
        if new_face_path not in self.encodings.keys():
            raise ValueError(f"Image '{new_face_path}' is not a registered face. Try extracting faces first.")

        task = {
            "total_comparisons": len(self.encodings)-1,
            "results": []
        }

        # Check previous comparisons
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(self.config.get_attribute("num_threads"))) as executor:
            all_futures = {}
            for known_face in sorted(self.encodings):
                if new_face_path != known_face: 
                    all_futures[
                        executor.submit(
                            self.compare_faces,
                            new_face_path,
                            known_face,
                            force_recalculation
                        )
                    ] = known_face

            for future in concurrent.futures.as_completed(all_futures):
                comparison = all_futures[future]
                try:
                    task["results"].append(
                        {
                            "known_face": comparison,
                            "similarity": future.result()
                        }
                    )
                except Exception as exc:
                    print(warning(f'{comparison} generated an exception: {exc}'))

        task["results"] = sorted(task["results"], key=lambda k: k["similarity"])
        return task
