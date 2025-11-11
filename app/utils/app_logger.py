import logging
import os


class AppLogger:
    def __init__(self, module_file: str, logger_file: str = "log.log"):
        """
        Inicializa un logger para el módulo actual.

        :param module_file: Ruta del archivo desde el que se crea el logger
            (ej. __file__).
        :param logger_file: Ruta del archivo de log donde se escribirán los
            logs
        """
        # solo el nombre del archivo
        module_name = os.path.basename(module_file)
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.DEBUG)  # nivel mínimo a registrar

        # Evitar duplicados si el logger ya tiene handlers
        if not self.logger.handlers:
            # Crear handler para archivo fijo con UTF-8
            file_handler = logging.FileHandler(logger_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)

            # Formato de los mensajes
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)

            # Agregar handler
            self.logger.addHandler(file_handler)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)
