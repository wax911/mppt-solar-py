import os
import sys
from itertools import zip_longest

import yaml
import logging
from pathlib import Path
from typing import Union, Optional, Any, Iterable, Sequence, Iterator
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter, StreamHandler, Logger

from dacite import from_dict


def group_items_into_chucks(
        data: Union[Iterable[Any], Sequence[Any]],
        segment_size: int,
        fill_missing_with: Optional[Any] = None
) -> Iterator[Any]:
    """
    Collect data into fixed-length chunks or blocks e.g.
    group_items_into_chucks('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    :param data: Iterable or sequence of data
    :param segment_size: Number of character per chunk
    :param fill_missing_with: Default fill value
    :return: Iterator of grouped items
    """
    args = [iter(data)] * segment_size
    return zip_longest(fillvalue=fill_missing_with, *args)


class FileSystem:

    @staticmethod
    def __get_base_dir():
        """At most all application packages are just one level deep"""
        current_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(current_path, '..', '..')

    @staticmethod
    def __get_config_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'settings')

    @staticmethod
    def get_plugins_directory() -> str:
        """
        Provides the path where plugins can be found
        :return: Path to the plugins folder
        """
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'plugins')

    @staticmethod
    def create_directory(directory_path: str) -> None:
        """
        Creates directories within the application main directory
        :param directory_path: Path of directory/directories that need to be created
        """
        creation_path = os.path.join(FileSystem.__get_base_dir(), directory_path)
        path = Path(creation_path)
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create_file(directory_path: str, filename: str) -> str:
        """
        Creates an empty file in the application main directory
        :param directory_path: Where the file should be written to
        :param filename: Name of file
        :return: The full path of where the file can be found
        """
        FileSystem.create_directory(directory_path)
        creation_path = os.path.join(FileSystem.__get_base_dir(), directory_path)
        file_path: str = os.path.join(creation_path, filename)
        Path(file_path).touch(exist_ok=True)
        return file_path

    @staticmethod
    def load_configuration(
            type_definition: type,
            name: str = 'settings.yaml',
            config_directory: Optional[str] = None
    ) -> Any:
        """
        Loads the configuration_ioc file and returns a configuration_ioc object
        :param type_definition: Type to convert to
        :param name: Name of the `yaml` file that contains the configuration_ioc, default is `settings.yaml`
        :param config_directory: Optional directory that contains the configuration_ioc file, default is `root/settings`
        :return: A configuration_ioc object
        """
        if config_directory is None:
            config_directory = FileSystem.__get_config_directory()
        with open(os.path.join(config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        # noinspection PyTypeChecker
        return from_dict(type_definition, input_data)


class Logging(Logger):
    __FORMATTER = "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"

    def __init__(
            self,
            name: str,
            log_file_name: str = 'mppt-solar',
            log_format: str = __FORMATTER,
            level: Union[int, str] = logging.DEBUG,
            *args,
            **kwargs
     ) -> None:
        super().__init__(name, level)
        self.formatter = Formatter(log_format)
        self.file_name = log_file_name
        self.addHandler(self.__get_stream_handler())
        self.addHandler(self.__get_file_handler())

    def __get_log_file(self) -> str:
        file_name = f'{self.file_name}.log'
        return FileSystem.create_file('logs', file_name)

    def __get_file_handler(self) -> TimedRotatingFileHandler:
        handler = TimedRotatingFileHandler(
            filename=self.__get_log_file(),
            when='midnight',
            backupCount=5
        )
        handler.setFormatter(self.formatter)
        return handler

    def __get_stream_handler(self) -> StreamHandler:
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(self.formatter)
        return handler


class LoggerFactory:

    def __init__(self, config) -> None:
        """
        :param config: Application configuration_ioc
        """
        self._verbosity = config.verbosity

    def create_logger(self, name: str) -> Logger:
        """
        Helper method that creates a logger instance using the supplied parameters
        :param name: The namespace of the calling module
        :return: Logger instance
        """
        logging.setLoggerClass(Logging)
        logger = logging.getLogger(name)
        logger.setLevel(self._verbosity)
        return logger
