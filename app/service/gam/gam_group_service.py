from app.utils.app_logger import AppLogger
from app.clients.gam.gam_client import GamClient

logger = AppLogger(__file__, "gam_service_group.log")


class GamGroupService:
    @staticmethod
    def create_group(group_email: str) -> bool:
        """Crea un grupo utilizando GAM, dado su correo electrónico"""
        command = ['gam', 'create', 'group', group_email]
        result = GamClient.call_gam_command(command)
        if result.returncode == 0:
            logger.info(f"Group {group_email} created successfully.")
            return True
        else:
            logger.error(f"Failed to create group {group_email}.")
            return False

    @staticmethod
    def delete_group(group_email: str) -> bool:
        """Elimina un grupo utilizando GAM, dado su correo electrónico"""
        command = ['gam', 'delete', 'group', group_email]
        result = GamClient.call_gam_command(command)
        if result.returncode == 0:
            logger.info(f"Group {group_email} deleted successfully.")
            return True
        else:
            logger.error(f"Failed to delete group {group_email}.")
            return False

    @staticmethod
    def add_user_owener_to_group(
            user_email: str, group_email: str, role: str
    ) -> bool:
        """Agrega un usuario a un grupo utilizando GAM"""
        command = [
            'gam', 'update', 'group', group_email,
            'add', 'owner', user_email
            ]
        result = GamClient.call_gam_command(command)
        if result.returncode == 0:
            logger.info(
                f"User {user_email} added to group {group_email} successfully."
            )
            return True
        else:
            logger.error(
                f"Failed to add user {user_email} to group {group_email}."
                )
            return False

    @staticmethod
    def add_user_member_to_group(
            user_email: str, group_email: str
    ) -> bool:
        """Agrega un usuario a un grupo utilizando GAM"""
        command = [
            'gam', 'update', 'group', group_email,
            'add', 'member', user_email
            ]
        result = GamClient.call_gam_command(command)
        if result.returncode == 0:
            logger.info(
                f"User {user_email} added to group {group_email} successfully."
            )
            return True
        else:
            logger.error(
                f"Failed to add user {user_email} to group {group_email}."
                )
            return False
