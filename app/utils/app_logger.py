import logging
import os
from typing import Optional


class AppLogger:
    def __init__(self, module_file: str, logger_file: Optional[str] = None):
        """
        Inicializa un logger para el módulo actual.

        :param module_file: Ruta del archivo desde el que se crea el logger
            (ej. __file__).
        :param logger_file: Nombre/ruta del archivo de log. Si no se envía,
            usa el nombre del módulo actual con extensión .log.
        """
        logs_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(logs_dir, exist_ok=True)

        module_name = os.path.basename(module_file)
        module_stem, _ = os.path.splitext(module_name)
        resolved_logger_file = logger_file or f"{module_stem}.log"

        log_path = os.path.join(logs_dir, resolved_logger_file)
        logger_key = f"{module_name}:{resolved_logger_file}"

        self.logger = logging.getLogger(logger_key)
        self.logger.setLevel(logging.DEBUG)  # nivel mínimo a registrar
        self.logger.propagate = False

        normalized_target = os.path.abspath(log_path).lower()
        has_target_handler = any(
            isinstance(h, logging.FileHandler)
            and os.path.abspath(h.baseFilename).lower() == normalized_target
            for h in self.logger.handlers
        )

        if not has_target_handler:
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def debug(self, msg: str, *args):
        self.logger.debug(msg, *args)

    def info(self, msg: str, *args):
        self.logger.info(msg, *args)

    def warning(self, msg: str, *args):
        self.logger.warning(msg, *args)

    def error(self, msg: str, *args):
        self.logger.error(msg, *args)

    def critical(self, msg: str, *args):
        self.logger.critical(msg, *args)
