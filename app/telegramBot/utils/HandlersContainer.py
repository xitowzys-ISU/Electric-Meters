import re
import importlib
from pathlib import Path
from loguru import logger as log


class HandlersContainer():
    """
    A class used to automatically create a handler container for ease of use in any file

    Attributes
    ----------
    path_handlers : str
        Path to the handlers folder

    Methods
    -------
    get_all_handlers()
        List of all handlers found
    """

    __instance = None

    def __new__(cls, path_handlers: str = None):
        if cls.__instance is None:
            cls.__instance = super(HandlersContainer, cls).__new__(cls)
            cls.__instance.__initialized = False

        return cls.__instance

    def __init__(self, path_handlers: str = None) -> None:

        if not self.__initialized:
            log.info("Создан контейнер обработчиков")
            self.__initialized = True

            self.__path_handlers: str = path_handlers
            self.__handlers: dict = {}
            self.__auto_init_handlers()
        else:
            return

    def __getitem__(self, key: int):
        """When double indexing returns the function of the handler method

        Returns
        -------
        function
            Handler Method function
        """

        return self.__handlers[key]

    def __auto_init_handlers(self):
        """Automatic search for created handlers and their methods"""

        self.__handlers = self.__search_handlers_methods(
            self.__search_files_handlers())

        pass

    def __search_files_handlers(self) -> dict:
        """Searches for handler files using the following template [name]Handler.py

        Returns
        -------
        dict
            Handlers files found
        """

        files = {}
        test_dir = Path(self.__path_handlers)

        for img_path in sorted(test_dir.glob("*.py")):
            result = re.search(r'handler\.py|handlers\.py',
                               img_path.name, flags=re.I)

            if result:
                files[img_path.name[:-3]] = {}

        # log.debug(files)
        return files

    def __search_handlers_methods(self, files: list):
        """Searches for handler methods

        Returns
        -------
        dict
            Updated dictionary with handler methods
        """

        for k, v in files.items():
            with open(f'{self.__path_handlers}/{k}.py', 'r', encoding='utf-8') as f:
                lines = f.read()
                results = re.finditer(
                    r'def\s+(\w+handler)[^\w+]', lines, flags=re.I)

                if results:
                    for result in results:
                        full_module_name = "app.telegramBot.handlers." + k

                        mymodule = importlib.import_module(
                            full_module_name)

                        files[k][result.group(1)] = getattr(
                            mymodule, result.group(1))

                        # log.debug(f"{result.group(1)}")

        return files

    def get_all_handlers(self):
        """List of all handlers found

        Returns
        -------
        list
            List with handlers
        """

        return self.__handlers.keys()
