from typing import List, Optional, Dict, Any
from app.utils.app_logger import AppLogger
from app.clients.gam.gam_client import GamClient
from app.domain.enums.gam_command_enum import GamCommandEnum

from app.domain.dtos.gam import GamUserDto

from app.service.gam.utils.gam_user_utils import (
    info_user,
    update_user_json,
    move_user_ou,
    update_user_groups,
    manage_licenses,
    get_drive_quota,
    suspend_user
)

logger = AppLogger(__file__, "gam_service_user.log")


class GamUserService:
    @staticmethod
    def crear_usuario(email: str) -> bool:
        """Crea un usuario utilizando GAM, dado su correo electrónico"""
        command = [
            GamCommandEnum.GAM.value,
            GamCommandEnum.CREATE.value,
            GamCommandEnum.USER.value,
            email,
        ]
        result = GamClient.call_gam_command(command)
        if result.returncode == 0:
            logger.info(f"User {email} created successfully.")
            return True
        else:
            logger.error(f"Failed to create user {email}.")
            return False

    @staticmethod
    def get_usuario_info_raw(email: str) -> str:
        """Obtiene información del usuario utilizando GAM (texto crudo)"""
        command = [
            GamCommandEnum.GAM.value,
            GamCommandEnum.INFO.value,
            GamCommandEnum.USER.value,
            email,
        ]
        result = GamClient.call_gam_command(command)
        return result.stdout

    @staticmethod
    def get_usuario_dto(email: str, quick: bool = False) -> GamUserDto:
        """Obtiene información del usuario en formato JSON y
        la parsea a GamUserDto (wrapper to module-level info_user)"""
        return info_user(email, quick=quick)

    @staticmethod
    def update_user_attributes(email: str, attrs: Dict[str, Any]) -> bool:
        """Actualiza atributos del usuario
        (wrapper to module-level update_user_json)"""
        result = update_user_json(email, attrs)
        return bool(result)

    @staticmethod
    def update_user_ou(
            email: str,
            org_unit_path: str,
            immutableous: Optional[List[str]] = None,
            preview: bool = False
    ) -> bool:
        """Wrapper to module-level move_user_ou"""
        immutableous_str = ",".join(immutableous) if immutableous else None
        result = move_user_ou(
            email,
            org_unit_path,
            immutableous=immutableous_str,
            preview=preview
        )
        return bool(result)

    @staticmethod
    def update_user_groups(
        email: str,
        add: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        role: Optional[str] = None
    ) -> bool:
        """Wrapper to module-level update_user_groups"""
        result = update_user_groups(email, add=add, remove=remove, role=role)
        return bool(result)

    @staticmethod
    def update_user_licenses(
        email: str,
        add: Optional[List[str]] = None,
        remove: Optional[List[str]] = None
    ) -> bool:
        """Wrapper to module-level manage_licenses"""
        result = manage_licenses(email, add=add, remove=remove)
        return bool(result)

    @staticmethod
    def get_user_quota(email: str) -> Dict[str, Any]:
        """Wrapper to module-level get_drive_quota"""
        return get_drive_quota(email)

    @staticmethod
    def suspend_user(email: str, suspend: bool = True) -> bool:
        """Wrapper to module-level suspend_user"""
        result = suspend_user(email, suspend=suspend)
        return bool(result)
