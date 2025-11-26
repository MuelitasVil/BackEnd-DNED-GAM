import asyncio
from typing import List
from app.utils.app_logger import AppLogger
from app.clients.gam.gam_client import GamClient
from app.domain.dtos.organization.email_dto import (
    EmailDTO as Email,
)

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
        
    @staticmethod
    async def manage_group(group_email: str, users: List[Email]) -> None:
        """
        Eliminar y crear el grupo, luego agregar los usuarios.
        El grupo es eliminado, creado y los usuarios agregados de forma concurrente.
        """
        # 1. Eliminar el grupo si existe
        GamGroupService.delete_group(group_email)

        # 2. Crear el grupo
        if not GamGroupService.create_group(group_email):
            logger.error(f"Failed to create group {group_email}.")
            return

        # 3. Procesar la adición de usuarios concurrentemente
        tasks = []

        # Para cada usuario en el grupo, se agrega según su rol
        for user_email in users.get('owner', []):  # Asumiendo que el rol 'owner' es una lista
            tasks.append(asyncio.to_thread(GamGroupService.add_user_owener_to_group, user_email, group_email))

        for user_email in users.get('member', []):  # Asumiendo que el rol 'member' es una lista
            tasks.append(asyncio.to_thread(GamGroupService.add_user_member_to_group, user_email, group_email))

        # Ejecutar todas las tareas concurrentemente
        await asyncio.gather(*tasks)

        logger.info(f"All users added to group {group_email}.")
