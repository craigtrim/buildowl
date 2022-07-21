#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Initialize a simple Disk-Backed Cache for OpenAI """


import os


from baseblock import EnvIO
from baseblock import FileIO
from baseblock import BaseObject


class OpenAICache(BaseObject):
    """ Initialize and Operate a simple Disk-Backed Cache for OpenAI """

    def __init__(self):
        """
        Created:
            20-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/6
        """
        BaseObject.__init__(self, __name__)
        self._cache_path = EnvIO.str_or_default(
            'AUTOSYN_CACHE_PATH', 'resources/cache/syns')
        FileIO.exists_or_create(self._cache_path)

    def _file_path(self,
                   file_name: str) -> str:
        def base() -> str:
            if len(file_name) >= 3:
                return os.path.join(self._cache_path,
                                    file_name[0],
                                    file_name[1],
                                    file_name[2])
            if len(file_name) >= 2:
                return os.path.join(self._cache_path,
                                    file_name[0],
                                    file_name[1])
            if len(file_name) >= 1:
                return os.path.join(self._cache_path,
                                    file_name[0])

        base_dir = base()

        FileIO.exists_or_create(base_dir)
        return os.path.join(base_dir, f"{file_name}.json")

    def exists(self,
               file_name: str) -> bool:
        """ Check if File exists in Cache

        Args:
            file_name (str): the file name

        Returns:
            bool: True if the file exists (this does not indicate if the file has content; only if the file exists)
        """
        try:
            file_path = self._file_path(file_name)
            return FileIO.exists(file_path)
        except TypeError as e:
            self.logger.error('\n'.join([
                "File Path Error",
                f"\tFile Name: {file_name}",
                f"\tError: {e}"]))
            return False

    def read(self,
             file_name: str) -> dict or list or None:
        """ Read Data from Cache

        Args:
            file_name (str): the file name

        Returns:
            dict or list or None: the JSON object (if any)
        """
        file_path = self._file_path(file_name)
        if FileIO.exists(file_path):
            return FileIO.read_json(file_path)

    def write(self,
              data: dict or list,
              file_name: str) -> None:
        """ Write Data to Cache

        Args:
            data (dict or list): the JSON object
            file_name (str): the name of the file to write
        """
        FileIO.write_json(data=data, file_path=self._file_path(file_name))
