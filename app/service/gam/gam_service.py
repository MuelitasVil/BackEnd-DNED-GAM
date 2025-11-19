import subprocess
import logging


class GamService:
    def __init__(self):
        # Configurar el logger para el servicio GAM
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _call_gam_command(self, command: list) -> subprocess.CompletedProcess:
        """Método interno para ejecutar un comando GAM"""
        try:
            # Ejecuta el comando GAM usando subprocess y captura la salida
            result = subprocess.run(command, text=True, capture_output=True, check=True)
            return result
        except subprocess.CalledProcessError as e:
            # Si hay un error, lo logeamos y lo retornamos
            self.logger.error(f"GAM command failed: {e}")
            return e

    def test_connection(self) -> bool:
        """Verifica la conexión con GAM ejecutando el comando 'gam version'"""
        command = ['gam', 'version']
        result = self._call_gam_command(command)
        if result.returncode == 0:
            self.logger.info("GAM connection is successful.")
            return True
        else:
            self.logger.error("Failed to connect to GAM.")
            return False

    def crear_usuario(self, email: str) -> bool:
        """Crea un usuario utilizando GAM, dado su correo electrónico"""
        command = ['gam', 'create', 'user', email]
        result = self._call_gam_command(command)
        if result.returncode == 0:
            self.logger.info(f"User {email} created successfully.")
            return True
        else:
            self.logger.error(f"Failed to create user {email}.")
            return False
