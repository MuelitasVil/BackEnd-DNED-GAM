from app.utils.app_logger import AppLogger
from app.clients.gam.gam_client import GamClient

logger = AppLogger(__file__, "gam_service_user.log")


class GamUserService:
    @staticmethod
    def crear_usuario(email: str) -> bool:
        """Crea un usuario utilizando GAM, dado su correo electrónico"""
        command = ['gam', 'create', 'user', email]
        result = GamClient.call_gam_command(command)
        if result.returncode == 0:
            logger.info(f"User {email} created successfully.")
            return True
        else:
            logger.error(f"Failed to create user {email}.")
            return False

    @staticmethod
    def get_usuario_info(email: str) -> str:
        """Obtiene información del usuario utilizando GAM"""
        command = ['gam', 'info', 'user', email]
        result = GamClient.call_gam_command(command)
        if result.returncode == 0:
            logger.info(f"User info for {email} retrieved successfully.")
            return result.stdout
        else:
            logger.error(f"Failed to retrieve info for user {email}.")
            return ""
