from loguru import logger as log
from telegram.ext import Handler
from telegram.ext import Dispatcher


class HandlersContainer():

    __instance = None

    def __new__(cls, dispatcher=None, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(
                HandlersContainer, cls).__new__(cls, *args, **kwargs)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, dispatcher=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.__initialized:
            self.__initialized = True

            if dispatcher:
                self.__dispatcher: Dispatcher = dispatcher
                self.__container: dict = dict()
            else:
                log.error(
                    "При перой инициализации контейнера должен передаваться dispatcher")
                exit(1)
        else:
            return

    def addHandler(self, handler: Handler, name_handler: str, isEnable: bool = True):

        self.__container[name_handler] = [handler, False]

        if isEnable is True:
            self.enableHandler(name_handler)
        else:
            self.enableHandler(name_handler)

        log.debug(
            f"Добавлен новый handler ({name_handler}): {self.__container}")

    def removeHandler(self, name_handler: str):
        self.disableHandler(name_handler)

        self.__container.pop(name_handler, None)

        log.debug(
            f"Удален handler ({name_handler}): {self.__container}")

    def disableHandler(self, name_handler: str):
        if self.__container[name_handler][1] is True:
            self.__container[name_handler][1] = False
            self.__dispatcher.remove_handler(self.__container[name_handler][0])

        log.debug(
            f"Выключен handler ({name_handler}): {self.__container}")

    def enableHandler(self, name_handler: str):
        if self.__container[name_handler][1] is False:
            self.__container[name_handler][1] = True
            self.__dispatcher.add_handler(self.__container[name_handler][0])

        log.debug(
            f"Включен handler ({name_handler}): {self.__container}")

    def getHandler(self, name_handler):
        return self.__container[name_handler][0]

    def disableAllHandler(self):
        for name_handler in self.__container.keys():
            self.disableHandler(name_handler)

        log.debug(
            f"Выключено все")
