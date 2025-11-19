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
            result = subprocess.run(
                command, text=True, capture_output=True, check=True
            )
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

    def get_usuario_info(self, email: str) -> str:
        """Obtiene información del usuario utilizando GAM"""
        command = ['gam', 'info', 'user', email]
        result = self._call_gam_command(command)
        if result.returncode == 0:
            self.logger.info(f"User info for {email} retrieved successfully.")
            return result.stdout
        else:
            self.logger.error(f"Failed to retrieve info for user {email}.")
            return ""

    def create_group(self, group_email: str) -> bool:
        """Crea un grupo utilizando GAM, dado su correo electrónico"""
        command = ['gam', 'create', 'group', group_email]
        result = self._call_gam_command(command)
        if result.returncode == 0:
            self.logger.info(f"Group {group_email} created successfully.")
            return True
        else:
            self.logger.error(f"Failed to create group {group_email}.")
            return False

    def delete_group(self, group_email: str) -> bool:
        """Elimina un grupo utilizando GAM, dado su correo electrónico"""
        command = ['gam', 'delete', 'group', group_email]
        result = self._call_gam_command(command)
        if result.returncode == 0:
            self.logger.info(f"Group {group_email} deleted successfully.")
            return True
        else:
            self.logger.error(f"Failed to delete group {group_email}.")
            return False

    def add_user_to_group(
            self, user_email: str, group_email: str, role: str
    ) -> bool:
        """Agrega un usuario a un grupo utilizando GAM"""
        command = [
            'gam', 'update', 'group', group_email,
            'add', 'member', user_email, 'role', role
            ]
        result = self._call_gam_command(command)
        if result.returncode == 0:
            self.logger.info(
                f"User {user_email} added to group {group_email} successfully."
            )
            return True
        else:
            self.logger.error(
                f"Failed to add user {user_email} to group {group_email}."
                )
            return False
