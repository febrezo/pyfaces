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
import sys

import configparser
from pathlib import Path


class ConfigManager:
    """Global configuration manager
    
    Attributes:
        {static} app_folder (str): The application folder where the information will be stored.
        {static} comparisons_file (str): The path to the file where the comparisons will be stored.
        {static} config (configparser.ConfigParser): The ConfigParser object.
        {static} config_file (str): The path to the file where the configuration will be stored.
        {static} encodings_file (str): The path to the file where the encodings will be stored.
        {static} faces_folder (str): The path to the folder where the faces images will be stored.
        {static} metadata_file (str): The path to the file where the metadata will be stored.
        {static} sources_folder (str): The path to the folder where the original images will be stored.
    """
    app_folder = None
    comparisons_file = None
    config = None
    config_file = None
    encodings_file = None
    faces_folder = None
    metadata_file = None
    sources_folder = None
    
    def __init__(self):
        """Constructor
        """
        if sys.platform == 'win32':
            self.app_folder = os.path.expanduser(os.path.join('~\\', 'Pyfaces'))
        else:
            self.app_folder = os.path.expanduser(os.path.join('~/', '.config', 'Pyfaces'))
        Path(self.app_folder).mkdir(parents=True, exist_ok=True)
                    
        self.config_file = os.path.join(self.app_folder, "config.ini")
        self.config = configparser.ConfigParser()
        if not self.config.read(self.config_file):
            self._initialize_configuration()
        self._update_paths()

    def _initialize_configuration(self):    
        """Initialize the configuration folder
        
        It also tries to create the files and folders.
        """       
        self.config = configparser.ConfigParser()
        self.config['Main Options'] = {
            "num_threads": os.cpu_count(),
            "data_folder": os.path.join(self.app_folder, "data")
        }
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)

    def _update_paths(self):
        self.faces_folder = os.path.join(self.get_attribute("data_folder"), "faces")
        self.sources_folder = os.path.join(self.get_attribute("data_folder"), "sources")
        self.encodings_file = os.path.join(self.get_attribute("data_folder"), "encodings.json")
        self.comparisons_file = os.path.join(self.get_attribute("data_folder"), "comparisons.json")
        self.metadata_file = os.path.join(self.get_attribute("data_folder"), "metadata.json")

        #Check that folders are created
        Path(self.faces_folder).mkdir(parents=True, exist_ok=True)
        Path(self.sources_folder).mkdir(parents=True, exist_ok=True)

    def get(self):
        """Recover all the configuration

        Returns:
            dict.
        """
        result = self.__dict__
        result["config"] = dict(self.config._sections)
        return result
        
    def get_attribute(self, name):
        """Get the value of an attribute in the configuration
        
        Args:
            name (str): Name of the attribute.

        Return:
            object.
        """
        return self.config.get("Main Options", name)
        
    def set_attribute(self, name, value):
        """Persist the value of an attribute in the configuration
        
        Args:
            name (str): Name of the attribute.
            value (str): Value.
            
        Raises:
            ValueError.
        """
        if name in ["num_threads", "data_folder"]:
            self.config.set("Main Options", name, str(value))
            with open(self.config_file, 'w') as config_file:
                self.config.write(config_file)
            self._update_paths()
        else:
            raise ValueError(f"The attribute '{name}' is not valid.")
